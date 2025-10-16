from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from lib.db import Base
import enum

class UserRole(enum.Enum):
    STUDENT = "student"
    TUTOR = "tutor"
    
class TutoringMode(enum.Enum):
    PHYSICAL = "physical"
    ONLINE = "online"
    BOTH = "both"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    location = Column(String(100), nullable=False)

     # student specific fields
    subjects_of_interest = Column(String(255), nullable=True)
    preferred_mode = Column(SQLEnum(TutoringMode), nullable=True)
    #tutor fields
    subjects = Column(String(255), nullable=True)
    qualifications = Column(String(255), nullable=True)
    hourly_rate = Column(Float, nullable=True)
    tutoring_mode = Column(SQLEnum(TutoringMode), nullable=True)
    availability = Column(String(100), default="Available")
   
    #tutor requests
    sent_requests = relationship('TutorRequest', foreign_keys='TutorRequest.student_id', back_populates='student')
    received_requests = relationship('TutorRequest', foreign_keys='TutorRequest.tutor_id', back_populates='tutor')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', role='{self.role.value}')>"
    
    def is_student(self):
        return self.role == UserRole.STUDENT
    
    def is_tutor(self):
        return self.role == UserRole.TUTOR

    def get_subjects_list(self):
        subjects_str = self.subjects if self.is_tutor() else self.subjects_of_interest
        if subjects_str:
            return [s.strip() for s in subjects_str.split(',')]
        return []
    
