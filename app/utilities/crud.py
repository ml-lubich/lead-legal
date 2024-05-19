from sqlalchemy.orm import Session
from .models import Lead

def create_lead(db: Session, lead: Lead):
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

def get_leads(db: Session):
    return db.query(Lead).all()

def update_lead_status(db: Session, lead_id: int, status: str):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead:
        lead.status = status
        db.commit()
        db.refresh(lead)
        return lead
    return None
