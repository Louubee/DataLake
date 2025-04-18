readme_content = """
# 🌐 DataLake API

Bienvenue dans l'API **DataLake**, une API RESTful développée avec **FastAPI**, permettant de gérer des **logs réseaux**, des **posts sociaux** et des **transactions clients**.  
L’API est sécurisée par **JWT**, avec des rôles (`user`, `admin`), un **quota horaire**, et une structure **versionnée** (`/v1`).

---

## 🚀 Fonctionnalités principales

- 🔐 Authentification par token JWT (`/register`, `/token`)
- 📉 Gestion de quota par utilisateur (100 requêtes/h)
- 📝 Logs réseaux (GET / PUT / DELETE)
- 📢 Réseaux sociaux (GET / PUT / DELETE)
- 💳 Transactions clients (GET / PUT / DELETE)
- ✅ Accès restreint par rôle (`admin` requis pour certaines routes)

---

## 🛠️ Technologies

- **FastAPI** + **Pydantic**
- **MongoDB** (via `pymongo`)
- **OAuth2PasswordRequestForm**
- **JWT Token Auth**
- **Quota / Rate limiting** personnalisé

---

## 📦 Installation

```bash
# 1. Cloner le repo
git clone https://github.com/Louube/datalake-api.git
cd datalake-api

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le serveur
uvicorn main:app --reload
