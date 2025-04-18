from database import social_collection
from models import SocialPost

def get_posts(skip: int = 0, limit: int = 10):
    return list(social_collection.find({}, {"_id": 0}).skip(skip).limit(limit))

def insert_post(post: SocialPost):
    result = social_collection.insert_one(post.dict())
    return str(result.inserted_id)

def get_post_by_id(post_id: str):
    return social_collection.find_one({"post_id": post_id}, {"_id": 0})

def delete_post_by_id(post_id: str):
    result = social_collection.delete_one({"post_id": post_id})
    return result.deleted_count

def update_post_by_id(post_id: str, post_data: dict):
    result = social_collection.update_one({"post_id": post_id}, {"$set": post_data})
    return result.modified_count

def count_posts():
    return social_collection.count_documents({})

def get_posts_by_user(user_id: str):
    return list(social_collection.find({"user.user_id": user_id}, {"_id": 0}))
