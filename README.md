# TutorMatch - Connecting Learners & Tutors
TutorMatch is a Python CLI application that helps students find tutors and tutors manage incoming requests. It provides registration, login, profile management, and a request workflow between students and tutors.

## Features
- Authentication
  - Student and tutor registration with validation
  - Login for both roles
- Profile management
  - Students and tutors can view and update their profiles
- Tutor requests
  - Students can view tutors and send tutor requests to the preferred tutor
  - Tutors can view and accept or reject requests sent to them
- Account deletion
  - Students and tutors can delete their accounts

## Tech Stack
- Language: Python
- ORM: SQLAlchemy
- Database: PostgresSQL
- Interface: CLI

## Getting Started

### 1. Clone and create a virtual environment
  - python3 -m venv venv
  - source venv/bin/activate

### 2. Install dependecies
- pip install -r requirements.txt

### 3. Initialize or reset the database
Start fresh database:
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








