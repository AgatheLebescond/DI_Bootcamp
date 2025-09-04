from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.bill import BillStatus, BillType

class BillBase(BaseModel):
    bill_number: str
    title: str
    short_title: Optional[str] = None
    summary: Optional[str] = None
    full_text_url: Optional[str] = None
    bill_type: BillType
    sponsor_id: Optional[int] = None
    introduced_date: Optional[datetime] = None

class BillCreate(BillBase):
    pass

class BillUpdate(BaseModel):
    title: Optional[str] = None
    short_title: Optional[str] = None
    summary: Optional[str] = None
    full_text_url: Optional[str] = None
    status: Optional[BillStatus] = None
    sponsor_id: Optional[int] = None
    house_passage_date: Optional[datetime] = None
    senate_passage_date: Optional[datetime] = None
    enacted_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class BillResponse(BillBase):
    id: int
    status: BillStatus
    house_passage_date: Optional[datetime]
    senate_passage_date: Optional[datetime]
    enacted_date: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True