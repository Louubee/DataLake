from fastapi import FastAPI, Body, HTTPException, Query, Depends, status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from models import LogEntry, SocialPost, Transaction
from crud import crud_logs, crud_social, crud_transactions
from rate_limiter import check_quota, MAX_REQUESTS
from auth import authenticate_user, create_access_token, hash_password, get_current_user, admin_required

from datetime import datetime, timedelta
from pydantic import BaseModel
from database import users_collection, usage_collection

api_v1 = APIRouter(prefix="/v1")

app = FastAPI(
    title="DataLake API",
    description="API d'un DataLake contenant des données issues de logs, de réseaux sociaux, et de transactions.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentification", "description": "Enregistrement, connexion et gestion du token"},
        {"name": "Quota", "description": "Affichage du quota d'utilisation de l'API"},
        {"name": "Logs", "description": "Opérations sur les logs réseaux"},
        {"name": "Social", "description": "Opérations sur les posts sociaux"},
        {"name": "Transactions", "description": "Opérations de transactions clients"},
    ]
)

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

@api_v1.post("/register", tags=["Authentification"])
def register_user(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")

    hashed = hash_password(user.password)
    users_collection.insert_one({
        "username": user.username,
        "hashed_password": hashed,
        "role": user.role
    })
    return {"message": "Utilisateur créé avec succès ✅"}

@api_v1.post("/token", tags=["Authentification"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Identifiants invalides")

    access_token_expires = timedelta(minutes=30)
    token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

@api_v1.get("/me/quota", tags=["Quota"])
def get_my_quota(current_user: dict = Depends(get_current_user)):
    usage = usage_collection.find_one({"username": current_user["username"]})
    now = datetime.utcnow()
    if not usage:
        return {"remaining": MAX_REQUESTS, "reset_in": "1h"}

    remaining = MAX_REQUESTS - usage["count"]
    reset_in = (usage["reset_time"] - now)
    return {
        "remaining": remaining,
        "reset_in_minutes": int(reset_in.total_seconds() / 60)
    }

@api_v1.get("/", tags=["Authentification"])
def root():
    return {"message": "Bienvenue sur l'API DataLake \U0001F680"}

# --- Logs ---
@api_v1.get("/logs/count", tags=["Logs"])
def count_logs(current_user: dict = Depends(get_current_user), _: None = Depends(check_quota)):
    return {"total_logs": crud_logs.count_logs()}

@api_v1.get("/logs/{ip}", tags=["Logs"])
def get_logs_by_ip(ip: str, current_user: dict = Depends(get_current_user)):
    logs = crud_logs.get_logs_by_ip(ip)
    if not logs:
        raise HTTPException(status_code=404, detail="Aucun log trouvé pour cette IP.")
    return logs

@api_v1.delete("/logs/{ip}", tags=["Logs"])
def delete_logs_by_ip(ip: str, current_user: dict = Depends(admin_required)):
    deleted = crud_logs.delete_logs_by_ip(ip)
    return {"deleted": deleted}

@api_v1.put("/logs/{ip}", tags=["Logs"])
def update_log_by_ip(ip: str, log_data: dict = Body(...), current_user: dict = Depends(admin_required)):
    updated = crud_logs.update_logs_by_ip(ip, log_data)
    if updated == 0:
        raise HTTPException(status_code=404, detail="Aucun log trouvé pour cette IP")
    return {"updated": updated}

# --- Social Media ---
@api_v1.get("/social/count", tags=["Social"])
def count_social_posts(current_user: dict = Depends(get_current_user)):
    return {"total_posts": crud_social.count_posts()}

@api_v1.get("/social/user/{user_id}", tags=["Social"])
def get_posts_by_user(user_id: str, current_user: dict = Depends(get_current_user)):
    posts = crud_social.get_posts_by_user(user_id)
    return posts


@api_v1.get("/social/{post_id}", tags=["Social"])
def get_post_by_id(post_id: str, current_user: dict = Depends(get_current_user)):
    post = crud_social.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    return post

@api_v1.delete("/social/{post_id}", tags=["Social"])
def delete_post_by_id(post_id: str, current_user: dict = Depends(admin_required)):
    deleted = crud_social.delete_post_by_id(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Aucun post supprimé")
    return {"deleted": deleted}

@api_v1.put("/social/{post_id}", tags=["Social"])
def update_post_by_id(post_id: str, post_data: dict = Body(...), current_user: dict = Depends(admin_required)):
    updated = crud_social.update_post_by_id(post_id, post_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Post non modifié")
    return {"updated": updated}

# --- Transactions ---
@api_v1.get("/transactions/count", tags=["Transactions"])
def count_transactions(current_user: dict = Depends(get_current_user)):
    return {"total_transactions": crud_transactions.count_transactions()}

@api_v1.get("/transactions/{client_id}", tags=["Transactions"])
def get_transaction(client_id: int, current_user: dict = Depends(get_current_user)):
    tx = crud_transactions.get_transaction_by_id(client_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    return tx

@api_v1.delete("/transactions/{client_id}", tags=["Transactions"])
def delete_transaction(client_id: int, current_user: dict = Depends(admin_required)):
    deleted = crud_transactions.delete_transaction_by_id(client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Aucune transaction supprimée")
    return {"deleted": deleted}

@api_v1.put("/transactions/{client_id}", tags=["Transactions"])
def update_transaction(client_id: int, data: dict = Body(...), current_user: dict = Depends(admin_required)):
    updated = crud_transactions.update_transaction_by_id(client_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Transaction non mise à jour")
    return {"updated": updated}

app.include_router(api_v1)
