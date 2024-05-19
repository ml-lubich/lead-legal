from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List

from .database import get_db  # Your database session creator
from .models import Lead  # Your ORM models for Lead
# Import Pydantic models
from .schemas import LeadCreate, LeadUpdate, LeadResponse, LeadStatusUpdate
from .utilities.email_service import send_email  # Email utilities
from .utilities.s3 import create_s3_client, upload_file_to_s3  # S3 utilities

app = FastAPI()
security = HTTPBasic()

SECRET_KEY = "secret"


def verify_secret(credentials: HTTPBasicCredentials):
    if credentials.password != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect security credentials",
            headers={"WWW-Authenticate": "Basic"}
        )


@app.post("/leads/", response_model=LeadResponse)
async def create_lead(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        resume: UploadFile = File(...),
        db: Session = Depends(get_db)):
    s3_client = create_s3_client()
    file_path = f"resumes/{email}_{resume.filename}"
    resume_url = upload_file_to_s3(s3_client, resume.file, file_path)

    if not resume_url:
        raise HTTPException(
            status_code=500, detail="Failed to upload resume to S3")

    new_lead = Lead(
        first_name=first_name,
        last_name=last_name,
        email=email,
        resume_url=resume_url,
        status="PENDING"
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    send_email(
        f"Thank you for submitting your application, {first_name}", "We have received your resume.", email)
    send_email("New Lead Alert",
               f"New lead {first_name} {last_name} added.", "leadlegalco@gmail.com", resume_url)

    return new_lead


@app.patch("/leads/{lead_id}/", response_model=LeadResponse)
async def update_lead(
        lead_id: int,
        update_data: LeadUpdate,
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)):
    verify_secret(credentials)
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Explicitly set all fields from update_data, assuming all fields can be optionally updated
    db_lead.first_name = update_data.first_name if update_data.first_name is not None else db_lead.first_name
    db_lead.last_name = update_data.last_name if update_data.last_name is not None else db_lead.last_name
    db_lead.email = update_data.email if update_data.email is not None else db_lead.email
    db_lead.status = update_data.status if update_data.status is not None else db_lead.status

    # Optional: Update resume if a new one is uploaded
    if update_data.resume:
        s3_client = create_s3_client()
        file_path = f"resumes/{update_data.email}_{update_data.resume.filename}"
        resume_url = upload_file_to_s3(
            s3_client, update_data.resume.file, file_path)
        if not resume_url:
            raise HTTPException(
                status_code=500, detail="Failed to upload resume to S3")
        db_lead.resume_url = resume_url

    db.commit()
    return db_lead


@app.patch("/leads/{lead_id}/status", response_model=LeadResponse)
async def update_lead_status(
        lead_id: int,
        status_update: LeadStatusUpdate,
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)):
    verify_secret(credentials)
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if status_update.status is not None:
        db_lead.status = status_update.status
        db.commit()
        return db_lead
    else:
        raise HTTPException(status_code=400, detail="No status provided")


@app.get("/leads/", response_model=List[LeadResponse])
async def list_leads(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    verify_secret(credentials)
    return db.query(Lead).all()
