from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# --- Model: Authentication ---


# --- Model: Logs ---
class LogEntry(BaseModel):
    ip_address: str = Field(..., alias="IP_Address")
    date: str
    time: str
    method: str
    url: str
    http_version: str = Field(..., alias="HTTP_Version")
    status_code: int = Field(..., alias="Status_Code")
    response_size: int = Field(..., alias="Response_Size")

# --- Model: Social Media ---
class Comment(BaseModel):
    comment_id: str
    user: str
    text: str
    timestamp: datetime

class User(BaseModel):
    user_id: str
    name: str
    followers: int

class SocialPost(BaseModel):
    post_id: str
    user: User
    content: str
    timestamp: datetime
    likes: int
    comments: List[Comment]

# --- Model: Transactions ---
class Transaction(BaseModel):
    client_id: int
    nom: str
    email: str
    date_inscription: str
