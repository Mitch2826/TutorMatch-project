from lib.db import get_session
from lib.models import Student, Tutor, TutorRequest, TutoringMode, RequestStatus

def test_models():
    session = get_session()
    
    try:
        # Test querying students
        print("\n Students:")
        students = session.query(Student).all()
        for student in students:
            print(f"  - {student.name} | Subjects: {student.subjects_of_interest}")
        
        # Test querying tutors
        print("\n Tutors:")
        tutors = session.query(Tutor).all()
        for tutor in tutors:
            print(f"  - {tutor.name} | Subjects: {tutor.subjects} | Rate: KES {tutor.hourly_rate}/hr")
        
        # Test creating a request
        if students and tutors:
            print("\n Creating a sample request...")
            request = TutorRequest(
                student_id=students[0].id,
                tutor_id=tutors[0].id,
                subject="Mathematics",
                mode="physical",
                message="I need help with calculus"
            )
            session.add(request)
            session.commit()
            print(f" Request created: Student '{students[0].name}' → Tutor '{tutors[0].name}'")
        
        # Test querying requests
        print("\n All Requests:")
        requests = session.query(TutorRequest).all()
        for req in requests:
            print(f"  - Request #{req.id}: {req.student.name} → {req.tutor.name} | Status: {req.status.value}")
        
    except Exception as e:
        print(f" Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    test_models()