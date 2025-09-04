#!/usr/bin/env python3
"""
Seed the database with sample data for testing
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
import random
from app.database import SessionLocal, engine
from app.models import Base, User, CongressMember, Bill, Vote
from app.models.congress_member import Party, Chamber
from app.models.bill import BillStatus, BillType
from app.models.vote import VoteType
from app.services.auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
db = SessionLocal()

def create_users():
    """Create sample users"""
    users = [
        {
            "username": "admin",
            "email": "admin@congressvote.com",
            "password": "admin123",
            "is_superuser": True
        },
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "is_superuser": False
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "password": "password123",
            "is_superuser": False
        }
    ]
    
    for user_data in users:
        user = db.query(User).filter(User.username == user_data["username"]).first()
        if not user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                is_superuser=user_data["is_superuser"]
            )
            db.add(user)
    
    db.commit()
    print("✓ Users created")

def create_congress_members():
    """Create sample congress members"""
    members_data = [
        # Senators
        {"first_name": "Chuck", "last_name": "Schumer", "party": Party.DEMOCRAT, "state": "NY", "chamber": Chamber.SENATE},
        {"first_name": "Mitch", "last_name": "McConnell", "party": Party.REPUBLICAN, "state": "KY", "chamber": Chamber.SENATE},
        {"first_name": "Bernie", "last_name": "Sanders", "party": Party.INDEPENDENT, "state": "VT", "chamber": Chamber.SENATE},
        {"first_name": "Elizabeth", "last_name": "Warren", "party": Party.DEMOCRAT, "state": "MA", "chamber": Chamber.SENATE},
        {"first_name": "Ted", "last_name": "Cruz", "party": Party.REPUBLICAN, "state": "TX", "chamber": Chamber.SENATE},
        
        # House Representatives
        {"first_name": "Nancy", "last_name": "Pelosi", "party": Party.DEMOCRAT, "state": "CA", "district": "11", "chamber": Chamber.HOUSE},
        {"first_name": "Kevin", "last_name": "McCarthy", "party": Party.REPUBLICAN, "state": "CA", "district": "20", "chamber": Chamber.HOUSE},
        {"first_name": "Alexandria", "last_name": "Ocasio-Cortez", "party": Party.DEMOCRAT, "state": "NY", "district": "14", "chamber": Chamber.HOUSE},
        {"first_name": "Matt", "last_name": "Gaetz", "party": Party.REPUBLICAN, "state": "FL", "district": "1", "chamber": Chamber.HOUSE},
        {"first_name": "Ilhan", "last_name": "Omar", "party": Party.DEMOCRAT, "state": "MN", "district": "5", "chamber": Chamber.HOUSE},
    ]
    
    created_members = []
    for member_data in members_data:
        full_name = f"{member_data['first_name']} {member_data['last_name']}"
        member = db.query(CongressMember).filter(CongressMember.full_name == full_name).first()
        if not member:
            member = CongressMember(
                **member_data,
                full_name=full_name,
                email=f"{member_data['first_name'].lower()}.{member_data['last_name'].lower()}@congress.gov",
                phone="(202) 555-0100",
                twitter_handle=f"@{member_data['last_name']}",
                website=f"https://www.{member_data['last_name'].lower()}.senate.gov"
            )
            db.add(member)
            created_members.append(member)
    
    db.commit()
    print("✓ Congress members created")
    return created_members

def create_bills():
    """Create sample bills"""
    bills_data = [
        {
            "bill_number": "H.R.1",
            "title": "For the People Act of 2023",
            "short_title": "For the People Act",
            "summary": "This bill addresses voter access, election integrity and security, campaign finance, and ethics for the three branches of government.",
            "bill_type": BillType.HOUSE_BILL,
            "status": BillStatus.PASSED_HOUSE,
            "introduced_date": datetime.now() - timedelta(days=90)
        },
        {
            "bill_number": "S.1",
            "title": "Infrastructure Investment and Jobs Act",
            "short_title": "Infrastructure Act",
            "summary": "This bill authorizes funds for Federal-aid highways, highway safety programs, and transit programs.",
            "bill_type": BillType.SENATE_BILL,
            "status": BillStatus.ENACTED,
            "introduced_date": datetime.now() - timedelta(days=180),
            "house_passage_date": datetime.now() - timedelta(days=120),
            "senate_passage_date": datetime.now() - timedelta(days=100),
            "enacted_date": datetime.now() - timedelta(days=80)
        },
        {
            "bill_number": "H.R.2",
            "title": "Secure the Border Act of 2023",
            "short_title": "Border Security Act",
            "summary": "This bill provides for operational control of the border, technology improvements, and increasing manpower.",
            "bill_type": BillType.HOUSE_BILL,
            "status": BillStatus.IN_COMMITTEE,
            "introduced_date": datetime.now() - timedelta(days=60)
        },
        {
            "bill_number": "S.2",
            "title": "America COMPETES Act of 2023",
            "short_title": "COMPETES Act",
            "summary": "This bill addresses U.S. competitiveness in science and technology, supply chain resilience, and manufacturing.",
            "bill_type": BillType.SENATE_BILL,
            "status": BillStatus.PASSED_SENATE,
            "introduced_date": datetime.now() - timedelta(days=120),
            "senate_passage_date": datetime.now() - timedelta(days=45)
        },
        {
            "bill_number": "H.J.Res.1",
            "title": "Proposing a balanced budget amendment to the Constitution",
            "short_title": "Balanced Budget Amendment",
            "summary": "This joint resolution proposes a constitutional amendment requiring a balanced federal budget.",
            "bill_type": BillType.HOUSE_JOINT_RESOLUTION,
            "status": BillStatus.INTRODUCED,
            "introduced_date": datetime.now() - timedelta(days=30)
        }
    ]
    
    created_bills = []
    for bill_data in bills_data:
        bill = db.query(Bill).filter(Bill.bill_number == bill_data["bill_number"]).first()
        if not bill:
            bill = Bill(**bill_data)
            db.add(bill)
            created_bills.append(bill)
    
    db.commit()
    print("✓ Bills created")
    return created_bills

def create_votes(members, bills):
    """Create sample votes"""
    vote_types = [VoteType.YEA, VoteType.NAY, VoteType.PRESENT, VoteType.NOT_VOTING]
    
    # Create votes for enacted bill (S.1)
    enacted_bill = next(b for b in bills if b.bill_number == "S.1")
    for member in members:
        # Democrats mostly vote Yea, Republicans mostly vote Nay
        if member.party == Party.DEMOCRAT:
            vote_type = random.choice([VoteType.YEA] * 9 + [VoteType.NAY])
        elif member.party == Party.REPUBLICAN:
            vote_type = random.choice([VoteType.NAY] * 8 + [VoteType.YEA] * 2)
        else:
            vote_type = random.choice([VoteType.YEA, VoteType.NAY])
        
        vote = Vote(
            bill_id=enacted_bill.id,
            congress_member_id=member.id,
            vote_type=vote_type,
            vote_date=enacted_bill.senate_passage_date if member.chamber == Chamber.SENATE else enacted_bill.house_passage_date
        )
        db.add(vote)
    
    # Create votes for passed house bill (H.R.1)
    house_bill = next(b for b in bills if b.bill_number == "H.R.1")
    house_members = [m for m in members if m.chamber == Chamber.HOUSE]
    for member in house_members:
        if member.party == Party.DEMOCRAT:
            vote_type = random.choice([VoteType.YEA] * 9 + [VoteType.NAY])
        else:
            vote_type = random.choice([VoteType.NAY] * 9 + [VoteType.YEA])
        
        vote = Vote(
            bill_id=house_bill.id,
            congress_member_id=member.id,
            vote_type=vote_type,
            vote_date=datetime.now() - timedelta(days=30)
        )
        db.add(vote)
    
    db.commit()
    print("✓ Votes created")

def main():
    """Main function to seed all data"""
    print("Seeding database...")
    
    try:
        create_users()
        members = create_congress_members()
        bills = create_bills()
        create_votes(members, bills)
        
        print("\n✅ Database seeded successfully!")
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()