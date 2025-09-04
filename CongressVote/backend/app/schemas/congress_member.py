from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.congress_member import Party, Chamber

class CongressMemberBase(BaseModel):
    first_name: str
    last_name: str
    full_name: str
    party: Party
    state: str
    district: Optional[str] = None
    chamber: Chamber
    email: Optional[str] = None
    phone: Optional[str] = None
    twitter_handle: Optional[str] = None
    website: Optional[str] = None

class CongressMemberCreate(CongressMemberBase):
    pass

class CongressMemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    party: Optional[Party] = None
    state: Optional[str] = None
    district: Optional[str] = None
    chamber: Optional[Chamber] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    twitter_handle: Optional[str] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None

class CongressMemberResponse(CongressMemberBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True