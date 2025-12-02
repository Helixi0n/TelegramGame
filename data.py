from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)
session = Session()
BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=0)
    name = Column(String)
    score = Column(Integer)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    time_completion = Column(String)

def init_db():
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)

def get_connection():
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()