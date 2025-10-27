from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database import Base

class VoteType(str, enum.Enum):
    YEA = "Yea"
    NAY = "Nay"
    PRESENT = "Present"
    NOT_VOTING = "Not Voting"

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    congress_member_id = Column(Integer, ForeignKey("congress_members.id"), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=False)
    vote_date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ensure one vote per member per bill
    __table_args__ = (UniqueConstraint('bill_id', 'congress_member_id', name='_bill_member_uc'),)
    
    # Relationships
    bill = relationship("Bill", back_populates="votes")
    congress_member = relationship("CongressMember", back_populates="votes")