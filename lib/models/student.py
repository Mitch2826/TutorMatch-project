from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from lib.db import Base
from datetime import datetime
import enum

class TutoringMode(enum.Enum):
    PHYSICAL = "physical"
    ONLINE = "online"
    BOTH = "both"
    
class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    location = Column(String(100), nullable=False)
    subjects_of_interest = Column(String(255), nullable=False)
    preferred_mode = Column(SQLEnum(TutoringMode), default=TutoringMode.BOTH)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tutor_requests = relationship('TutorRequest', back_populates='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    def get_subjects_list(self):
        #returns a list of subjects of interest
        return [s.strip() for s in self.subjects_of_interest.split(',')]