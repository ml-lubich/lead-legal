from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class LeadCreate(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")

class LeadUpdate(BaseModel):
    first_name: Optional[str] = Field(None, example="Jane")
    last_name: Optional[str] = Field(None, example="Smith")
    email: Optional[EmailStr] = Field(None, example="jane.smith@example.com")
    status: Optional[str] = Field(None, example="REACHED_OUT")

class LeadResponse(BaseModel):
    id: int = Field(..., example=1)
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    resume_url: Optional[str] = Field(None, example="https://example.com/resume.pdf")
    status: str = Field(..., example="PENDING")

    class Config:
        orm_mode = True

class LeadStatusUpdate(BaseModel):
    status: Optional[str] = Field(None, example="REACHED_OUT", description="The new status of the lead")

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")

class TokenData(BaseModel):
    username: Optional[str] = Field(None, example="admin")
