from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from ..models.vote import VoteType

class VoteBase(BaseModel):
    bill_id: int
    congress_member_id: int
    vote_type: VoteType
    vote_date: datetime
    notes: Optional[str] = None

class VoteCreate(VoteBase):
    pass

class VoteUpdate(BaseModel):
    vote_type: Optional[VoteType] = None
    vote_date: Optional[datetime] = None
    notes: Optional[str] = None

class VoteResponse(VoteBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class VoteStats(BaseModel):
    bill_id: int
    total_votes: int
    yea_votes: int
    nay_votes: int
    present_votes: int
    not_voting: int
    vote_breakdown: Dict[str, int]
    party_breakdown: Dict[str, Dict[str, int]]