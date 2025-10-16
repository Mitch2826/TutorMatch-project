from lib.models import Student, Tutor, TutorRequest, RequestStatus
import sys
#student dashboard
class StudentMenu:
    def __init__(self, session, student):
        self.session = session
        self.student = student
    def clear_screen(self):
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
        
    def display_header(self):
        print("\n" + "="*50)
        print(f"        ** Welcome, {self.student.name}! **")
        print("="*50 + "\n")
    def student_menu(self):
        while True:
            self.clear_screen()
            self.display_header()
            
            print("1. Find a Tutor")
            print("2. View My Requests")
            print("3. View My Profile")
            print("4. Update My Profile")
            print("5. Logout")
            print("-" * 50)
            
            choice = input("Select an option (1-5): ").strip()
            
            if choice == "1":
                self.find_tutor()
            elif choice == "2":
                self.view_my_requests()
            elif choice == "3":
                self.view_my_requests()
            elif choice == "4":
                self.update_profile()
            elif choice == "5":
                self.logout()
                break
            else:
                input("Invalid option. Press Enter to try again...")
    #find and request a tutor
    def find_tutor(self):
        self.clear_screen()
        self.display_header()
        print ("FIND A TUTOR\n")
        
        print("Filter Options:")
        print("1. By Subject")
        print("2. By Location")
        print("3. By Tutoring Mode")
        print("4. View All Tutors")
        print("5. Back to Menu")
        print("-" * 50)
        
        choice = input("Select filter (1-5): ").strip()
        
        if choice == "1":
            self.find_by_subject()
        elif choice == "2":
            self.find_by_location()
        elif choice == "3":
            self.find_by_mode()
        elif choice == "4":
            self.view_all_tutors()
        elif choice == "5":
            return
        else:
            input("Invalid option. Press Enter to continue...")
    
    def find_by_subject():
        pass
    def find_by_location():
        pass
    def find_by_mode():
        pass
    def view_all_tutors():
        pass
    def display_tutors():
        pass
    def display_tutors_and_request():
        pass
    def request_tutor():
        pass
    def view_my_requests():
        pass
    def view_profile():
        pass
    def update_profile():
        pass
    def logout():
        pass
    def display():
        pass