from database import transactions_collection
from models import Transaction

def get_transactions(skip: int = 0, limit: int = 10):
    return list(transactions_collection.find({}, {"_id": 0}).skip(skip).limit(limit))

def insert_transaction(tx: Transaction):
    result = transactions_collection.insert_one(tx.dict())
    return str(result.inserted_id)

def get_transaction_by_id(client_id: int):
    return transactions_collection.find_one({"client_id": client_id}, {"_id": 0})

def delete_transaction_by_id(client_id: int):
    result = transactions_collection.delete_one({"client_id": client_id})
    return result.deleted_count

def update_transaction_by_id(client_id: int, data: dict):
    result = transactions_collection.update_one({"client_id": client_id}, {"$set": data})
    return result.modified_count

def count_transactions():
    return transactions_collection.count_documents({})

def search_transaction_by_email(email: str):
    return transactions_collection.find_one({"email": email}, {"_id": 0})
