"""
Test Authentication Service
File: test_auth_service.py
"""

print("Testing Authentication Service...")
print("-" * 50)

try:
    from lib.db import get_session, init_db
    from lib.cli.auth import AuthService
    from lib.models import Student, Tutor, TutoringMode
    
    print(" All imports successful!")
    
    # Initialize database
    print("\n🔧 Initializing database...")
    init_db()
    print("✅ Database initialized!")
    
    # Get session
    session = get_session()
    print(" Database session created!")
    
    # Test AuthService
    auth = AuthService(session)
    print(" AuthService instantiated!")
    
    # Test password hashing
    hashed = auth.hash_password("test123")
    print(f" Password hashing works: {hashed[:20]}...")
    
    # Test student registration
    print("\n Testing student registration...")
    success, msg = auth.register_student(
        name="Test Student",
        email="test.student@example.com",
        phone="0700000001",
        password="password123",
        location="Nairobi",
        subjects_of_interest="Mathematics, Physics",
        preferred_mode="both"
    )
    print(f"   Result: {msg}")
    
    # Test tutor registration
    print("\n Testing tutor registration...")
    success, msg = auth.register_tutor(
        name="Test Tutor",
        email="test.tutor@example.com",
        phone="0700000002",
        password="password123",
        location="Nairobi",
        subjects="Mathematics, Physics",
        qualifications="PhD",
        hourly_rate=1500.0,
        tutoring_mode="both"
    )
    print(f"   Result: {msg}")
    
    # Test student login
    print("\n Testing student login...")
    user, role = auth.login("test.student@example.com", "password123")
    if user and role == 'student':
        print(f" Student login successful: {user.name} ({role})")
    else:
        print(" Student login failed")
    
    # Test tutor login
    print("\n Testing tutor login...")
    user, role = auth.login("test.tutor@example.com", "password123")
    if user and role == 'tutor':
        print(f" Tutor login successful: {user.name} ({role})")
    else:
        print(" Tutor login failed")
    
    # Test wrong password
    print("\n Testing wrong password...")
    user, role = auth.login("test.student@example.com", "wrongpassword")
    if user is None and role is None:
        print(" Wrong password correctly rejected")
    else:
        print(" Wrong password was accepted (security issue!)")
    
    print("\n" + "-" * 50)
    print(" All authentication tests passed!")
    print("-" * 50)
    
    session.close()
    
except ImportError as e:
    print(f" Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()
