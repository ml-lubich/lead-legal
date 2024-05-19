from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    status = Column(String, default='PENDING')
    resume_url = Column(Text)