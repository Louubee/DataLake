# 🌐 DataLake

Ce projet est une solution complète de **DataLake** qui combine :
- Un système de collecte de données via **Kafka** pour l'ingestion de données en temps réel
- Un stockage persistant sur **MongoDB Atlas**
- Une **API RESTful** pour l'accès et la gestion des données

## 📊 Architecture du DataLake

### Sources de données
- Fichiers CSV/JSON/SQLITE en temps réel
- Streams de données réseaux
- Données de transactions
- Posts des réseaux sociaux

### Pipeline de données
1. **Producers Kafka** : Ingestion des données depuis différentes sources
2. **Topics Kafka** : Organisation des données par type (logs, transactions, posts)
3. **Consumers Kafka** : Traitement et transformation des données
4. **MongoDB Atlas** : Stockage persistant des données structurées

## 🚀 Fonctionnalités principales

### DataLake
- 🔄 Ingestion en temps réel via Kafka
- 📥 Multiples sources de données supportées
- 🔄 Transformation des données en vol
- 💾 Stockage optimisé sur MongoDB Atlas

### API RESTful
- 🔐 Authentification par token JWT (`/register`, `/token`)
- 📉 Gestion de quota par utilisateur (100 requêtes/h)
- 📝 Logs réseaux (GET / PUT / DELETE)
- 📢 Réseaux sociaux (GET / PUT / DELETE)
- 💳 Transactions clients (GET / PUT / DELETE)
- ✅ Accès restreint par rôle (`admin` requis pour certaines routes)

## 🛠️ Technologies

### DataLake
- **Apache Kafka** pour l'ingestion de données
- **Kafka Connect** pour la connexion aux sources
- **MongoDB Atlas** pour le stockage
- **Python** pour les consumers/producers

### API
- **FastAPI** + **Pydantic**
- **OAuth2PasswordRequestForm**
- **JWT Token Auth**
- **Quota / Rate limiting** personnalisé

## 📦 Installation

```bash
# 1. Cloner le repo
git clone https://github.com/Louube/datalake-api.git
cd datalake-api

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer Kafka
# Assurez-vous que Kafka est installé et en cours d'exécution
# Configurez les variables d'environnement dans .env

# 4. Lancer les consumers Kafka
python kafka/consumers/main.py

# 5. Lancer l'API
uvicorn main:app --reload
```

## 🔧 Configuration

### Variables d'environnement requises
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
MONGO_URI=your_mongodb_uri
JWT_SECRET=your_jwt_secret
```

### Structure des topics Kafka
- `network_logs` : Logs réseaux
- `social_posts` : Posts des réseaux sociaux
- `transactions` : Transactions clients
