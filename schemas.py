from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# User schema
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    account_number: str
    iban: str

class UserInDB(UserCreate):
    id: int
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Blacklist schema
class BlacklistCreate(BaseModel):
    user_id: int
    reason: Optional[str] = None

class BlacklistInDB(BlacklistCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    status: Optional[bool] = None

    class Config:
        from_attributes = True
