from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database import Base

class BillStatus(str, enum.Enum):
    INTRODUCED = "Introduced"
    IN_COMMITTEE = "In Committee"
    PASSED_HOUSE = "Passed House"
    PASSED_SENATE = "Passed Senate"
    TO_PRESIDENT = "To President"
    SIGNED = "Signed"
    VETOED = "Vetoed"
    ENACTED = "Enacted"

class BillType(str, enum.Enum):
    HOUSE_BILL = "H.R."
    SENATE_BILL = "S."
    HOUSE_JOINT_RESOLUTION = "H.J.Res."
    SENATE_JOINT_RESOLUTION = "S.J.Res."
    HOUSE_CONCURRENT_RESOLUTION = "H.Con.Res."
    SENATE_CONCURRENT_RESOLUTION = "S.Con.Res."
    HOUSE_RESOLUTION = "H.Res."
    SENATE_RESOLUTION = "S.Res."

class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    short_title = Column(String)
    summary = Column(Text)
    full_text_url = Column(String)
    bill_type = Column(Enum(BillType), nullable=False)
    status = Column(Enum(BillStatus), default=BillStatus.INTRODUCED)
    sponsor_id = Column(Integer)  # Reference to CongressMember
    introduced_date = Column(DateTime(timezone=True))
    house_passage_date = Column(DateTime(timezone=True))
    senate_passage_date = Column(DateTime(timezone=True))
    enacted_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    votes = relationship("Vote", back_populates="bill")