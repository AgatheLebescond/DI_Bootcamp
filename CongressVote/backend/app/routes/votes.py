from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Vote, Bill, CongressMember, User
from ..models.vote import VoteType
from ..schemas.vote import VoteCreate, VoteUpdate, VoteResponse, VoteStats
from ..services.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[VoteResponse])
def get_votes(
    skip: int = 0,
    limit: int = 100,
    bill_id: Optional[int] = None,
    congress_member_id: Optional[int] = None,
    vote_type: Optional[VoteType] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Vote)
    
    if bill_id:
        query = query.filter(Vote.bill_id == bill_id)
    if congress_member_id:
        query = query.filter(Vote.congress_member_id == congress_member_id)
    if vote_type:
        query = query.filter(Vote.vote_type == vote_type)
    
    votes = query.order_by(Vote.vote_date.desc()).offset(skip).limit(limit).all()
    return votes

@router.get("/stats/{bill_id}", response_model=VoteStats)
def get_vote_stats(bill_id: int, db: Session = Depends(get_db)):
    # Check if bill exists
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Get vote counts
    vote_counts = db.query(
        Vote.vote_type,
        func.count(Vote.id).label('count')
    ).filter(Vote.bill_id == bill_id).group_by(Vote.vote_type).all()
    
    # Initialize stats
    stats = {
        "bill_id": bill_id,
        "total_votes": 0,
        "yea_votes": 0,
        "nay_votes": 0,
        "present_votes": 0,
        "not_voting": 0,
        "vote_breakdown": {},
        "party_breakdown": {}
    }
    
    # Process vote counts
    for vote_type, count in vote_counts:
        stats["vote_breakdown"][vote_type.value] = count
        stats["total_votes"] += count
        
        if vote_type == VoteType.YEA:
            stats["yea_votes"] = count
        elif vote_type == VoteType.NAY:
            stats["nay_votes"] = count
        elif vote_type == VoteType.PRESENT:
            stats["present_votes"] = count
        elif vote_type == VoteType.NOT_VOTING:
            stats["not_voting"] = count
    
    # Get party breakdown
    party_votes = db.query(
        CongressMember.party,
        Vote.vote_type,
        func.count(Vote.id).label('count')
    ).join(
        CongressMember, Vote.congress_member_id == CongressMember.id
    ).filter(Vote.bill_id == bill_id).group_by(
        CongressMember.party, Vote.vote_type
    ).all()
    
    for party, vote_type, count in party_votes:
        if party.value not in stats["party_breakdown"]:
            stats["party_breakdown"][party.value] = {}
        stats["party_breakdown"][party.value][vote_type.value] = count
    
    return VoteStats(**stats)

@router.post("/", response_model=VoteResponse)
def create_vote(
    vote: VoteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if bill exists
    bill = db.query(Bill).filter(Bill.id == vote.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Check if congress member exists
    member = db.query(CongressMember).filter(CongressMember.id == vote.congress_member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Congress member not found")
    
    # Check if vote already exists
    existing_vote = db.query(Vote).filter(
        Vote.bill_id == vote.bill_id,
        Vote.congress_member_id == vote.congress_member_id
    ).first()
    if existing_vote:
        raise HTTPException(status_code=400, detail="Vote already exists for this member on this bill")
    
    db_vote = Vote(**vote.dict())
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

@router.put("/{vote_id}", response_model=VoteResponse)
def update_vote(
    vote_id: int,
    vote_update: VoteUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    vote = db.query(Vote).filter(Vote.id == vote_id).first()
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    update_data = vote_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vote, field, value)
    
    db.commit()
    db.refresh(vote)
    return vote

@router.delete("/{vote_id}")
def delete_vote(
    vote_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    vote = db.query(Vote).filter(Vote.id == vote_id).first()
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    db.delete(vote)
    db.commit()
    return {"message": "Vote deleted successfully"}