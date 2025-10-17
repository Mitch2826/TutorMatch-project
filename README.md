# TutorMatch - Connecting Learners & Tutors
TutorMatch is a Python CLI application that helps students find tutors and tutors manage incoming requests. It provides registration, login, profile management, and a request workflow between students and tutors.

## Features
- Student and Tutor registration and login
- Tutor profile management (subjects, qualifications, hourly rate, availability, tutoring mode)
- Students can create tutoring requests
- Tutors can review and accept or reject requests

## Tech Stack
- Python
- SQLAlchemy ORM
- PostgresSQL

## Getting Started

### 1. Clone and create a virtual environment
- Windows:
  - py -3.11 -m venv .venv
  - .\.venv\Scripts\activate

- Linux/macOS/WSL:
  - python3 -m venv venv
  - source venv/bin/activate

### 2. Install dependecies
- pip install -r requirements.txt

### 3. Initialize or reset the database
Run the seeder:
- python -m lib.seed

Menu options:
- 1. Initialize fresh database (create tables + seed data)
- 2. Reset database (DELETE ALL DATA and reinitialize)
- 3. Exit

The seed script creates:
- Sample students
- Sample tutors
- Sample tutor requests

It will print test credentials at the end. Use those to log in.

### 4. Run the CLI
- python run.py

Main menu:
- Register as Student
- Register as Tutor
- Login
- Exit

After login:
- Students see the student dashboard/menu
- Tutors see the tutor dashboard/menu

Tutor menu highlights:
- View My Requests
- View/Update Profile
- View All Students Requesting Me
- Logout

## Data Model (overview)

- Student
  - name, email (unique), phone, location
  - subjects_of_interest
  - preferred_mode
- Tutor
  - name, email (unique), phone, location
  - subjects, qualifications, hourly_rate
  - tutoring_mode
  - availability
- TutorRequest
  - Relationships: Student -> Tutor
  - status (PENDING, REJECTED, ACCEPTED)




