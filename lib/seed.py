from lib.db import engine, Base, get_session
from lib.models import Student, Tutor, TutorRequest,TutoringMode, RequestStatus
from lib.cli import AuthService
def create_tables():
    #create all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    
def seed_sample_data():
    session = get_session()
    
    try:
        if session.query(Student).count() > 0 or session.query(Tutor).count() > 0:
            print(" !Database already has data. Skipping seed.")
            return
        auth_service = AuthService(session)
        
        print(" Creating sample students...\n")
        
        #students
        student1_success, student1_msg = auth_service.register_student(
            name="Brian Otieno",
            email="brian.otieno@tutormatch.co.ke",
            phone="0712345678",
            password="B0tieno123",
            location="Nairobi",
            subjects_of_interest="Mathematics, Physics, Computer Studies",
            preferred_mode="both"
        )
        print(f"   {student1_msg}")
        
        student2_success, student2_msg = auth_service.register_student(
            name="Aisha Mohamed",
            email="aisha.mohamed@tutormatch.co.ke",
            phone="0723456789",
            password="password123",
            location="Mombasa",
            subjects_of_interest="English, Swahili, History",
            preferred_mode="online"
        )
        print(f"   {student2_msg}")
        
        student3_success, student3_msg = auth_service.register_student(
            name="Kevin Kipruto",
            email="kevin.kipruto@tutormatch.co.ke",
            phone="0734567890",
            password="password123",
            location="Eldoret",
            subjects_of_interest="Biology, Chemistry, Agriculture",
            preferred_mode="physical"
        )
        print(f"   {student3_msg}\n")
        
        #tutors
        tutor1_success, tutor1_msg = auth_service.register_tutor(
            name="Dr. Mercy Wanjiku",
            email="mercy.wanjiku@tutormatch.co.ke",
            phone="0745678901",
            password="WanMercy123",
            location="Nairobi",
            subjects="Mathematics, Physics, Computer Studies",
            qualifications="PhD in Applied Mathematics, 8 years experience",
            hourly_rate=800.0,
            tutoring_mode="both"
        )
        print(f"   {tutor1_msg}")
        
        tutor2_success, tutor2_msg = auth_service.register_tutor(
            name="Mr. Daniel Odhiambo",
            email="daniel.odhiambo@tutormatch.co.ke",
            phone="0756789012",
            password="password123",
            location="Kisumu",
            subjects="English, Literature, Swahili",
            qualifications="BA in Education (English & Kiswahili), 6 years experience",
            hourly_rate=500.0,
            tutoring_mode="online"
        )
        print(f"   {tutor2_msg}")
        
        tutor3_success, tutor3_msg = auth_service.register_tutor(
            name="Ms. Lucy Njeri",
            email="lucy.njeri@tutormatch.co.ke",
            phone="0767890123",
            password="password123",
            location="Nakuru",
            subjects="Biology, Chemistry, Agriculture",
            qualifications="MSc in Biology, 5 years experience",
            hourly_rate=1000.0,
            tutoring_mode="physical"
        )
        print(f"   {tutor3_msg}")
        
        tutor4_success, tutor4_msg = auth_service.register_tutor(
            name="Mr. Hassan Abdi",
            email="hassan.abdi@tutormatch.co.ke",
            phone="0778901234",
            password="password123",
            location="Garissa",
            subjects="Islamic Studies, History, Geography",
            qualifications="BA in Humanities, 7 years experience",
            hourly_rate=450.0,
            tutoring_mode="both"
        )
        print(f"   {tutor4_msg}\n")
        
        #new session to fetch users
        session.close()
        session = get_session()
        
        #get students and tutors
        students = session.query(Student).all()
        tutors = session.query(Tutor).all()
        #requests
        if students and tutors:
            # Create sample requests
            request1 = TutorRequest(
                student_id=students[0].id,
                tutor_id=tutors[0].id,
                subject="Mathematics",
                mode="physical",
                message="I need help understanding calculus and trigonometry for KCSE prep.",
                status=RequestStatus.PENDING
            )
            session.add(request1)
            
            request2 = TutorRequest(
                student_id=students[1].id,
                tutor_id=tutors[1].id,
                subject="Swahili",
                mode="online",
                message="Looking for help in writing Kiswahili compositions.",
                status=RequestStatus.ACCEPTED
            )
            session.add(request2)
            
            request3 = TutorRequest(
                student_id=students[2].id,
                tutor_id=tutors[2].id,
                subject="Biology",
                mode="physical",
                message="Need help revising for biology practicals.",
                status=RequestStatus.PENDING
            )
            session.add(request3)
            
            session.commit()
            print(" Sample tutor requests created.\n")
            
        print("="*50)
        print(" DATABASE SEEDED SUCCESSFULLY!")
        print("="*50)
        print(f"    {len(students)} students created")
        print(f"    {len(tutors)} tutors created")
        print(f"    {len(session.query(TutorRequest).all())} sample requests created\n")
        print("  Test Credentials:")
        print("   Student: brian.otieno@gmail.com / password123")
        print("   Tutor:   mercy.wanjiku@gmail.com / WanMercy123")
        print("="*50 + "\n")
        
    except Exception as e:
        session.rollback()
        print(f" Error seeding data: {e}\n")
    finally:
        session.close()
        
def reset_database():
        
    print("\n" + "="*50)
    print("  WARNING: This will DELETE ALL DATA!")
    print("="*50)
    confirm = input("\nType 'YES' to confirm reset: ").strip()
        
    if confirm == "YES":
        try:
            print("\n  Dropping all tables...")
            Base.metadata.drop_all(bind=engine)
            print(" Tables dropped!")
            print()
            create_tables()
            seed_sample_data()
        except Exception as e:
            print(f" Error during reset: {e}\n")
    else:  
        print(" Operation cancelled.\n") 
        
if __name__ == "__main__":
    
    print("\n" + "="*50)
    print("   TutorMatch - DB Initialization 🇰🇪")
    print("="*50 + "\n")
        
    print("1. Initialize fresh database (create tables + seed data)")
    print("2. Reset database (DELETE ALL DATA and reinitialize)")
    print("3. Exit")
    print("-"*50)
        
    choice = input("Select option (1-3): ").strip()
        
    if choice == "1":  
        create_tables()
        seed_sample_data()
        
    elif choice == "2":
        
        reset_database()
    elif choice == "3":
        print("Exiting...\n")
    else:
        print(" Invalid option.\n")
        
        
        
    print("-"*50)
        
    choice = input("Select option (1-3): ").strip()
        
    if choice == "1":
        
        create_tables()
        seed_sample_data()
    elif choice == "2": 
        reset_database()
    elif choice == "3":
        print("Exiting...\n")
    else:
        print(" Invalid option.\n")
        
    