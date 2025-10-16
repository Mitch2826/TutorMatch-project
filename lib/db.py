from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_session():
    return SessionLocal()
def init_db():
   
    from lib.models import Student, Tutor, TutorRequest  # import models here
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

