import hashlib
from sqlalchemy.exc import IntegrityError
from lib.models.student import Student
from lib.models.tutor import Tutor
from lib.models.enums import TutoringMode

class AuthService: 
    def __init__(self, session):
        self.session = session
    #store passwords securely
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def email_exists_student(self, email):
        #check if email already registered as student
        return self.session.query(Student).filter_by(email=email).first() is not None
    
    def email_exists_tutor(self, email):
        #check if email is already registered as tutor
        return self.session.query(Tutor).filter_by(email=email).first() is not None
    
    def email_exists(self, email):
        #check if email exists in either table
        return self.email_exists_student(email) or self.email_exists_tutor(email)
    
    #register student
    def register_student(self, name, email, phone, password, location, 
                        subjects_of_interest, preferred_mode):
        
        try:
            if self.email_exists(email):
                return False, "Email already registered!"
            
            if not all([name, email, phone, password, location, subjects_of_interest]):
                return False, "All fields are required!"
            
            student = Student(
                name=name,
                email=email,
                phone=phone,
                password=self.hash_password(password),
                location=location,
                subjects_of_interest=subjects_of_interest,
                preferred_mode=TutoringMode[preferred_mode.upper()]
            )
            
            self.session.add(student)
            self.session.commit()
            
            return True, f"Student '{name}' registered successfully!"
        
        except IntegrityError:
            self.session.rollback()
            return False, "Email already exists!"
        except Exception as e:
            self.session.rollback()
            return False, f"Registration failed: {str(e)}"
        
    #register tutor
    def register_tutor(self, name, email, phone, password, location, subjects,
                      qualifications, hourly_rate, tutoring_mode):

        try:
            if self.email_exists(email):
                return False, "Email already registered!"
            
            if not all([name, email, phone, password, location, subjects, 
                       qualifications, hourly_rate]):
                return False, "All fields are required!"
            
            if hourly_rate <= 0:
                return False, "Hourly rate must be greater than 0!"
            
            tutor = Tutor(
                name=name,
                email=email,
                phone=phone,
                password=self.hash_password(password),
                location=location,
                subjects=subjects,
                qualifications=qualifications,
                hourly_rate=hourly_rate,
                tutoring_mode=TutoringMode[tutoring_mode.upper()]
            )
            
            self.session.add(tutor)
            self.session.commit()
            
            return True, f"Tutor '{name}' registered successfully!"
        
        except IntegrityError:
            self.session.rollback()
            return False, "Email already exists!"
        except Exception as e:
            self.session.rollback()
            return False, f"Registration failed: {str(e)}" 
         
    def login_student(self, email, password):      
        try:
            if not email or not password:
                return None
            
            student = self.session.query(Student).filter_by(email=email).first()
            
            if student and student.password == self.hash_password(password):
                return student
            
            return None
        
        except Exception as e:
            print(f"Login error: {str(e)}")
            return None
    #tutor login
    def login_tutor(self, email, password):
        try:
            if not email or not password:
                return None
            
            tutor = self.session.query(Tutor).filter_by(email=email).first()
            
            if tutor and tutor.password == self.hash_password(password):
                return tutor
            
            return None
        
        except Exception as e:
            print(f"Login error: {str(e)}")
            return None
        
    def login(self, email, password):
        try:
            if not email or not password:
                return None, None
            
            #student login first
            student = self.login_student(email, password)
            if student:
                return student, 'student'
            
            #tutor login
            tutor = self.login_tutor(email, password)
            if tutor:
                return tutor, 'tutor'
            
            return None, None
        
        except Exception as e:
            print(f"Login error: {str(e)}")
            return None, None