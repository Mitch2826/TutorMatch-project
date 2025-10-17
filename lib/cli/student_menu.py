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
    
    def find_by_subject(self):
        self.clear_screen()
        self.display_header()
        print("FIND TUTORS BY SUBJECT\n")
        
        subject = input("Enter subject to search: ").strip().lower()
        
        if not subject:
            input("Subject cannot be empty. Press Enter to continue...")
            return
        
        tutors = self.session.query(Tutor).all()
        matching_tutors = [t for t in tutors if t.offers_subject(subject)]
        
        if matching_tutors:
            self.display_tutors_and_request(matching_tutors, subject)
        else:
            print(f"No tutors found for '{subject}'")
            input("Press Enter to continue...")
        
    def find_by_location(self):
        self.clear_screen()
        self.display_header()
        print("FIND TUTORS BY LOCATION\n")
        
        location = input("Enter location to search: ").strip().lower()
        
        if not location:
            input("Location cannot be empty. Press Enter to continue...")
            return
        
        tutors = self.session.query(Tutor).filter(
            Tutor.location.ilike(f"%{location}%")
        ).all()
        
        if tutors:
            self.display_tutors(tutors)
        else:
            print(f"No tutors found in '{location}'")
            input("Press Enter to continue...")
            
        
    def find_by_mode(self):
        self.clear_screen()
        self.display_header()
        print("FIND TUTORS BY TUTORING MODE\n")
        
        print("1. Physical (In-person)")
        print("2. Online")
        print("3. Both")
        print("-" * 50)
        
        choice = input("Select mode (1-3): ").strip()
        mode_map = {"1": "PHYSICAL", "2": "ONLINE", "3": "BOTH"}
        
        if choice not in mode_map:
            input("Invalid option. Press Enter to continue...")
            return
        
        from lib.models import TutoringMode
        selected_mode = TutoringMode[mode_map[choice]]
        
        tutors = self.session.query(Tutor).filter(
            Tutor.tutoring_mode.in_([selected_mode, TutoringMode.BOTH])
        ).all()
        
        if tutors:
            self.display_tutors(tutors)
        else:
            print(f"No tutors found with that mode")
            input("Press Enter to continue...")
    
    
    def view_all_tutors(self):
        tutors = self.session.query(Tutor).all()
        
        if tutors:
            self.display_tutors(tutors)
        else:
            print("No tutors available at the moment.")
            input("Press Enter to continue...")
        
    def display_tutors(self, tutors):
        self.clear_screen()
        self.display_header()
        print(f"FOUND {len(tutors)} TUTOR(S)\n")
        
        for idx, tutor in enumerate(tutors, 1):
            print(f"{idx}. {tutor.name}")
            print(f"  Location: {tutor.location}")
            print(f"  Subjects: {tutor.subjects}")
            print(f"  Rate: KES {tutor.hourly_rate}/hr")
            print(f"  Qualifications: {tutor.qualifications}")
            print(f"  Mode: {tutor.tutoring_mode.value}")
            print()
        
        choice = input("Enter tutor number to request (or 'back'): ").strip()
        
        if choice.lower() == 'back':
            return
        
        try:
            tutor_idx = int(choice) - 1
            if 0 <= tutor_idx < len(tutors):
                self.request_tutor(tutors[tutor_idx])
            else:
                input("Invalid selection Press Enter to continue...")   
        except ValueError:
            input("Invalid input. Press Enter to continue...")
    
    def display_tutors_and_request(self, tutors, subject):
        self.clear_screen()
        self.display_header()
        print(f"FOUND {len(tutors)} TUTOR(S) FOR '{subject}'\n")
        
        for idx, tutor in enumerate(tutors, 1):
            print(f"{idx}. {tutor.name}")
            print(f"  Location: {tutor.location}")
            print(f"  Subjects: {tutor.subjects}")
            print(f"  Rate: KES {tutor.hourly_rate}/hr")
            print(f"  Qualifications: {tutor.qualifications}")
            print(f"  Mode: {tutor.tutoring_mode.value}")
            print()
        
        choice = input("Enter tutor number to request (or 'back'): ").strip()
        
        if choice.lower() == 'back':
            return
        
        try:
            tutor_idx = int(choice) - 1
            if 0 <= tutor_idx < len(tutors):
                self.request_tutor(tutors[tutor_idx], subject)
            else:
                input("Invalid selection Press Enter to continue...")   
        except ValueError:
            input("Invalid input. Press Enter to continue...")
    
    
    def request_tutor(self, tutor, subject=None):
        self.clear_screen()
        self.display_header()
        print(f"REQUEST TUTOR: {tutor.name}\n")
        
        if not subject:
            subject = input("Subject needed help with: ").strip()
        
        print("\nPreferred Tutoring Mode:")
        print("1. Physical (In-person)")
        print("2. Online")
        mode_choice = input("Select mode (1-2): ").strip()
        
        mode_map = {"1": "physical", "2": "online"}
        mode = mode_map.get(mode_choice, "physical")
        
        message = input("\nAdditional Message (optional): ").strip()
        
        try:
            # check if already requested this tutor
            existing = self.session.query(TutorRequest).filter_by(
                student_id=self.student.id,
                tutor_id=tutor.id
            ).first()
            
            if existing:
                print(" You've already sent a request to this tutor!")
                input("Press Enter to continue...")
                return
            
            request = TutorRequest(
                student_id=self.student.id,
                tutor_id=tutor.id,
                subject=subject,
                mode=mode,
                message=message if message else None
            )
            
            self.session.add(request)
            self.session.commit()
            
            print(f"\n Request sent to {tutor.name}!")
            print("   They'll respond shortly.")
            input("Press Enter to continue...")
        
        except Exception as e:
            self.session.rollback()
            print(f" Error sending request: {str(e)}")
            input("Press Enter to continue...")
            
    def view_my_requests(self):
        self.clear_screen()
        self.display_header()
        print(" MY TUTOR REQUESTS\n")
        
        requests = self.session.query(TutorRequest).filter_by(
            student_id=self.student.id
        ).all()
        
        if not requests:
            print("You haven't sent any requests yet.")
            input("Press Enter to continue...")
            return
        
        for idx, req in enumerate(requests, 1):
            
            print(f"   Subject: {req.subject}")
            print(f"   Mode: {req.mode}")
            print(f"   Status: {req.status.value.upper()}")
            print(f"   Requested: {req.created_at.strftime('%Y-%m-%d %H:%M')}")
                
            if req.message:
                print(f"   Your message: {req.message}")
            print()
        
    input("Press Enter to continue...")
    
    
    def view_profile(self):
        self.clear_screen()
        self.display_header()
        print(" MY PROFILE\n")
        
        print(f"Name: {self.student.name}")
        print(f"Email: {self.student.email}")
        print(f"Phone: {self.student.phone}")
        print(f"Location: {self.student.location}")
        print(f"Subjects of Interest: {self.student.subjects_of_interest}")
        print(f"Preferred Mode: {self.student.preferred_mode.value}")
        
        input("\nPress Enter to continue...")
    
    def update_profile(self):
        self.clear_screen()
        self.display_header()
        print(" UPDATE PROFILE\n")
        
        print("What would you like to update?")
        print("1. Subjects of Interest")
        print("2. Preferred Tutoring Mode")
        print("3. Location")
        print("4. Back to Menu")
        print("-" * 50)
        
        choice = input("Select (1-4): ").strip()
        
        try:
            if choice == "1":
                new_subjects = input("New subjects (comma-separated): ").strip()
                if new_subjects:
                    self.student.subjects_of_interest = new_subjects
                    self.session.commit()
                    print(" Subjects updated!")
            
            elif choice == "2":
                print("\n1. Physical\n2. Online\n3. Both")
                mode_choice = input("Select (1-3): ").strip()
                mode_map = {"1": "physical", "2": "online", "3": "both"}
                if mode_choice in mode_map:
                    from lib.models import TutoringMode
                    self.student.preferred_mode = TutoringMode[mode_map[mode_choice].upper()]
                    self.session.commit()
                    print(" Tutoring mode updated!")
            
            elif choice == "3":
                new_location = input("New location: ").strip()
                if new_location:
                    self.student.location = new_location
                    self.session.commit()
                    print(" Location updated!")
            
            elif choice == "4":
                return
            
            input("Press Enter to continue...")
        
        except Exception as e:
            self.session.rollback()
            print(f" Error updating profile: {str(e)}")
            input("Press Enter to continue...")
        
    
    #logout and return to main menu
    def logout(self):
        print("\n Logged out successfully!")
        input("Press Enter to return to main menu...")
        
     
    def display(self):
        self.student_menu()