from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CongressMember
from ..models.congress_member import Chamber, Party
from ..schemas.congress_member import CongressMemberCreate, CongressMemberUpdate, CongressMemberResponse
from ..services.auth import get_current_active_user, get_current_user
from ..models import User

router = APIRouter()

@router.get("/", response_model=List[CongressMemberResponse])
def get_congress_members(
    skip: int = 0,
    limit: int = 100,
    chamber: Optional[Chamber] = None,
    party: Optional[Party] = None,
    state: Optional[str] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    query = db.query(CongressMember)
    
    if chamber:
        query = query.filter(CongressMember.chamber == chamber)
    if party:
        query = query.filter(CongressMember.party == party)
    if state:
        query = query.filter(CongressMember.state == state.upper())
    if is_active is not None:
        query = query.filter(CongressMember.is_active == is_active)
    
    members = query.offset(skip).limit(limit).all()
    return members

@router.get("/{member_id}", response_model=CongressMemberResponse)
def get_congress_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(CongressMember).filter(CongressMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Congress member not found")
    return member

@router.post("/", response_model=CongressMemberResponse)
def create_congress_member(
    member: CongressMemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_member = CongressMember(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@router.put("/{member_id}", response_model=CongressMemberResponse)
def update_congress_member(
    member_id: int,
    member_update: CongressMemberUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    member = db.query(CongressMember).filter(CongressMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Congress member not found")
    
    update_data = member_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(member, field, value)
    
    db.commit()
    db.refresh(member)
    return member

@router.delete("/{member_id}")
def delete_congress_member(
    member_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    member = db.query(CongressMember).filter(CongressMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Congress member not found")
    
    member.is_active = False
    db.commit()
    return {"message": "Congress member deactivated successfully"}