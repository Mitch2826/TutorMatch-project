from lib.db import engine, Base, get_session
from lib.models import Student, Tutor, TutorRequest,TutoringMode, RequestStatus

def create_tables():
    #create all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    
def seed_sample_data():
    session = get_session()
    