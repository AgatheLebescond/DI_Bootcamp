from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Bill, User
from ..models.bill import BillStatus, BillType
from ..schemas.bill import BillCreate, BillUpdate, BillResponse
from ..services.auth import get_current_active_user, get_current_user

router = APIRouter()

@router.get("/", response_model=List[BillResponse])
def get_bills(
    skip: int = 0,
    limit: int = 100,
    status: Optional[BillStatus] = None,
    bill_type: Optional[BillType] = None,
    sponsor_id: Optional[int] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    query = db.query(Bill)
    
    if status:
        query = query.filter(Bill.status == status)
    if bill_type:
        query = query.filter(Bill.bill_type == bill_type)
    if sponsor_id:
        query = query.filter(Bill.sponsor_id == sponsor_id)
    if is_active is not None:
        query = query.filter(Bill.is_active == is_active)
    
    bills = query.order_by(Bill.introduced_date.desc()).offset(skip).limit(limit).all()
    return bills

@router.get("/{bill_id}", response_model=BillResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

@router.get("/by-number/{bill_number}", response_model=BillResponse)
def get_bill_by_number(bill_number: str, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_number == bill_number).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

@router.post("/", response_model=BillResponse)
def create_bill(
    bill: BillCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if bill number already exists
    existing_bill = db.query(Bill).filter(Bill.bill_number == bill.bill_number).first()
    if existing_bill:
        raise HTTPException(status_code=400, detail="Bill number already exists")
    
    db_bill = Bill(**bill.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(
    bill_id: int,
    bill_update: BillUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    update_data = bill_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bill, field, value)
    
    db.commit()
    db.refresh(bill)
    return bill

@router.delete("/{bill_id}")
def delete_bill(
    bill_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    bill.is_active = False
    db.commit()
    return {"message": "Bill deactivated successfully"}