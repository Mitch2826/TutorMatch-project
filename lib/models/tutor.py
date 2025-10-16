from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from lib.db import Base
from datetime import datetime
import enum

class TutoringMode(enum.Enum):
    PHYSICAL = "physical"
    ONLINE = "online"
    BOTH = "both"
    
class Tutor(Base):
    __tablename__ = 'tutors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    location = Column(String(100), nullable=False)
    subjects = Column(String(255), nullable=False)
    qualifications = Column(String(255), nullable=False)
    hourly_rate = Column(Float, nullable=False)
    tutoring_mode = Column(SQLEnum(TutoringMode), default=TutoringMode.BOTH)
    availability = Column(String(100), default="Available")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    #relations
    tutor_requests = relationship('TutorRequest', back_populates='tutor', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Tutor(id={self.id}, name='{self.name}', email='{self.email}', rate={self.hourly_rate})>"
    
    def get_subjects_list(self):
        #Returns subjects list
        return [s.strip() for s in self.subjects.split(',')]
    
    def offers_subject(self, subject):
        #check if a tutor offers a specific subject
        return subject.lower() in [s.lower() for s in self.get_subjects_list()]
    