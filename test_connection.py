from lib.db import get_session
from sqlalchemy import text

def test_connection():
    session = None
    try:
        session = get_session()
        session.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    test_connection()
