from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from lib.db import Base
from datetime import datetime,timezone
import enum 

class RequestStatus(enum.Enum):
    #status of the tutoring request
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    
class TutorRequest(Base):
    #tutor requests from students to tutors
    __tablename__ = 'tutor_requests'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    tutor_id = Column(Integer, ForeignKey('tutors.id'), nullable=False)
    subject = Column(String(100), nullable=False)
    mode = Column(String(20), nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)
    message = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    #relations
    student = relationship('Student', foreign_keys=[student_id], back_populates='tutor_requests')
    tutor = relationship('Tutor', foreign_keys=[tutor_id], back_populates='tutor_requests')
    
    def __repr__(self):
        return f"<TutorRequest(id={self.id}, student_id={self.student_id}, tutor_id={self.tutor_id}, status='{self.status.value}')>"
    
    def accept(self):
        self.status = RequestStatus.ACCEPTED
        self.updated_at = lambda: datetime.now(timezone.utc)()
        
    def reject(self):
        self.status = RequestStatus.REJECTED
        self.updated_at = lambda: datetime.now(timezone.utc)()
    
    def complete(self):
        self.status = RequestStatus.COMPLETED
        self.updated_at = lambda: datetime.now(timezone.utc)()