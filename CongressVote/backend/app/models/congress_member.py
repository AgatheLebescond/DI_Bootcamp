from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database import Base

class Party(str, enum.Enum):
    DEMOCRAT = "Democrat"
    REPUBLICAN = "Republican"
    INDEPENDENT = "Independent"
    OTHER = "Other"

class Chamber(str, enum.Enum):
    HOUSE = "House"
    SENATE = "Senate"

class CongressMember(Base):
    __tablename__ = "congress_members"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    party = Column(Enum(Party), nullable=False)
    state = Column(String(2), nullable=False)
    district = Column(String, nullable=True)  # For House members
    chamber = Column(Enum(Chamber), nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    twitter_handle = Column(String)
    website = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    votes = relationship("Vote", back_populates="congress_member")