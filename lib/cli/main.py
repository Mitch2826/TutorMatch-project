from lib.db import get_session
from lib.models import Student, Tutor, TutoringMode
from lib.cli.auth import AuthService
from lib.cli.student_menu import StudentMenu
from lib.cli.tutor_menu import TutorMenu
import sys

class TutorMatchCLI:
    def __init__(self):
        self.session = get_session()
        self.auth_service = AuthService(self.session)
        self.current_user = None
    def display_header(self):
        """Display app header"""
        print("\n" + "="*50)
        print("        ** TUTORMATCH - Connecting Learners & Tutors **")
        print("="*50 + "\n")
    def clear_screen(self):
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
    def main_menu(self):
        while True:
            self.clear_screen()
            self.display_header()
            print("Welcome to TutorMatch!\n")
            print("1. Register as Student")
            print("2. Register as Tutor")
            print("3. Login")
            print("4. Exit")
            print("-" * 50)
            
            choice = input("Select an option (1-4): ").strip()
            
            if choice == "1":
                self.register_student()
            elif choice == "2":
                self.register_tutor()
            elif choice == "3":
                self.login()
            elif choice == "4":
                self.exit_app()
            else:
                input("Invalid option. Press Enter to try again...")
    #student registration
    def register_student(self):
        self.clear_screen()
        self.display_header()
        print("STUDENT REGISTRATION\n")
        
        try:
            name = input("Full Name: ").strip()
            if not name:
                print("Name cannot be empty!")
                input("Press Enter to continue...")
                return
            
            email = input("Email: ").strip()
            phone = input("Phone Number: ").strip()
            password = input("Password: ").strip()
            confirm_password = input("Confirm Password: ").strip()
            
            if password != confirm_password:
                print("Passwords don't match!")
                input("Press Enter to continue...")
                return
            
            location = input("Location (e.g., Nairobi, Mombasa): ").strip()
            subjects = input("Subjects of Interest (comma separate): ").strip()
            
            print("\nPreferred Tutoring Mode:")
            print("1. Physical (In-person)")
            print("2. Online")
            print("3. Both")
            mode_choice = input("Select (1-3): ").strip()
            
            mode_map = {"1": "physical", "2": "online", "3": "both"}
            preferred_mode = mode_map.get(mode_choice, "both")
            
            success, message = self.auth_service.register_student(
                name, email, phone, password, location, subjects, preferred_mode
            )
            if success:
                print(f"\n {message}")
                input("Press Enter to return to main menu...")
            else:
                print(f"\n {message}")
                input("Press Enter to try again...")
        
        except Exception as e:
            print(f" Error: {str(e)}")
            input("Press Enter to continue...")
            
    #tutor registration
    def register_tutor(self):
        self.clear_screen()
        self.display_header()
        print(" TUTOR REGISTRATION\n")
        
        try:
            name = input("Full Name: ").strip()
            if not name:
                print(" Name cannot be empty!")
                input("Press Enter to continue...")
                return
            
            email = input("Email: ").strip()
            phone = input("Phone Number: ").strip()
            password = input("Password: ").strip()
            confirm_password = input("Confirm Password: ").strip()
            
            if password != confirm_password:
                print(" Passwords don't match!")
                input("Press Enter to continue...")
                return
            
            location = input("Location (e.g., Nairobi, Mombasa): ").strip()
            subjects = input("Subjects You Teach (comma-separated): ").strip()
            qualifications = input("Qualifications: ").strip()
            
            try:
                hourly_rate = float(input("Hourly Rate (KES): ").strip())
            except ValueError:
                print(" Invalid rate. Please enter a number.")
                input("Press Enter to continue...")
                return
            
            print("\nTutoring Mode:")
            print("1. Physical (In-person)")
            print("2. Online")
            print("3. Both")
            mode_choice = input("Select (1-3): ").strip()
            
            mode_map = {"1": "physical", "2": "online", "3": "both"}
            tutoring_mode = mode_map.get(mode_choice, "both")
            
            success, message = self.auth_service.register_tutor(
                name, email, phone, password, location, subjects, 
                qualifications, hourly_rate, tutoring_mode
            )
            
            if success:
                print(f"\n {message}")
                input("Press Enter to return to main menu...")
            else:
                print(f"\n {message}")
                input("Press Enter to try again...")
        
        except Exception as e:
            print(f" Error: {str(e)}")
            input("Press Enter to continue...")
            
    def login(self):
        self.clear_screen()
        self.display_header()
        print(" LOGIN\n")
        
        try:
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            user, role = self.auth_service.login(email, password)
            
            if user:
                self.current_user = user
                print(f"\n Welcome {user.name}!")
                input("Press Enter to continue...")
                
                if role == 'student':
                    self.student_dashboard()
                else:
                    self.tutor_dashboard()
            else:
                print("\n Invalid email or password!")
                input("Press Enter to try again...")
            
        except Exception as e:
            print(f" Error: {str(e)}")
            input("Press Enter to continue...")
    def student_dashboard(self):
        student_menu = StudentMenu(self.session, self.current_user)
        student_menu.display()
        self.current_user = None
        
    def tutor_dashboard(self):
        tutor_menu = TutorMenu(self.session, self.current_user)
        tutor_menu.display()
        self.current_user = None
        
    def exit_app(self):
        self.clear_screen()
        print("\n" + "="*50)
        print("Thank you for using TutorMatch!")
        print("Goodbye! 👋")
        print("="*50 + "\n")
        self.session.close()
        sys.exit(0)
        
    def run(self):
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n")
            self.exit_app()
        except Exception as e:
            print(f" Unexpected error: {str(e)}")
            self.session.close()
    sys.exit(1)

def main():
    #entry
    app = TutorMatchCLI()
    app.run()

if __name__ == "__main__":
    main()        
            