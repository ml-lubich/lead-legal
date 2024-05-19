from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    resume_url = Column(Text)
    status = Column(String, default='PENDING')

def get_engine(db_url):
    return create_engine(db_url)

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables(engine):
    Base.metadata.create_all(engine)
