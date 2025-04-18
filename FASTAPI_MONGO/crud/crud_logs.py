from database import logs_collection
from models import LogEntry

def insert_log(log: LogEntry):
    result = logs_collection.insert_one(log.dict(by_alias=True))
    return str(result.inserted_id)

def get_logs(skip: int = 0, limit: int = 10):
    return list(logs_collection.find({}, {"_id": 0}).skip(skip).limit(limit))

def get_logs_by_ip(ip: str):
    return list(logs_collection.find({"IP_Address": ip}, {"_id": 0}))

def delete_logs_by_ip(ip: str):
    result = logs_collection.delete_many({"IP_Address": ip})
    return result.deleted_count
'''
def delete_all_logs():
    result = logs_collection.delete_many({})
    return result.deleted_count'''

def count_logs():
    return logs_collection.count_documents({})
