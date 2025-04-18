from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from database import usage_collection
from auth import get_current_user

MAX_REQUESTS = 100
WINDOW_DURATION = timedelta(hours=1)

def check_quota(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    usage = usage_collection.find_one({"username": username})
    now = datetime.utcnow()
    if current_user["role"] == "admin":
        max_requests = 500 
    else:
        max_requests = 100  

    if not usage:
        # Première fois, on initialise
        usage_collection.insert_one({
            "username": username,
            "count": 1,
            "reset_time": now + WINDOW_DURATION
        })
        return

    # Période expirée → on réinitialise
    if now > usage["reset_time"]:
        usage_collection.update_one(
            {"username": username},
            {"$set": {"count": 1, "reset_time": now + WINDOW_DURATION}}
        )
        return

    # Encore dans la fenêtre → on incrémente ou on bloque
    if usage["count"] >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Quota de requêtes dépassé. Réessaie plus tard.")
    
    usage_collection.update_one(
        {"username": username},
        {"$inc": {"count": 1}}
    )
