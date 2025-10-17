from lib.models import Student, Tutor, TutorRequest, RequestStatus
import sys

#tutor dashboard
class TutorMenu:
    def __init__(self,session, tutor):
        self.session = session
        self.tutor = tutor
        
    def clear_screen(self):
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
        
    def display_header(self): 
        print("\n" + "="*100)
        print(f"         TUTOR DASHBOARD - {self.tutor.name}")
        print("="*100 + "\n")
        
    #display tutor menu options
    def tutor_menu(self):
        while True:
            self.clear_screen()
            self.display_header()
            
            #count pending requests
            pending_count = self.session.query(TutorRequest).filter_by(
                tutor_id=self.tutor.id,
                status=RequestStatus.PENDING
            ).count()
            
            print("1. View My Requests")
            if pending_count > 0:
                print(f" {pending_count} pending request(s)!")
            print("2. View My Profile")
            print("3. Update My Profile")
            print("4. View All Students Requesting Me")
            print("5. Delete My Account")
            print("6. Logout")
            print("-" * 50)
            
            choice = input("Select an option (1-6): ").strip()
            
            if choice == "1":
                self.view_my_requests()
            elif choice == "2":
                self.view_profile()
            elif choice == "3":
                self.update_profile()
            elif choice == "4":
                self.view_all_students()
            elif choice == "5":
                if self.delete_account():
                    break
            elif choice == "6":
                self.logout()
                break
            else:
                input(" Invalid option. Press Enter to try again...")
    
    #view tutor requests         
    def view_my_requests(self):
        self.clear_screen()
        self.display_header()
        print(" MY TUTORING REQUESTS\n")
        
        requests = self.session.query(TutorRequest).filter_by(
            tutor_id=self.tutor.id
        ).all()
        
        if not requests:
            print("No requests received yet.")
            input("Press Enter to continue...")
            return
        #categorize requests by status
        pending = [r for r in requests if r.status == RequestStatus.PENDING]
        accepted = [r for r in requests if r.status == RequestStatus.ACCEPTED]
        rejected = [r for r in requests if r.status == RequestStatus.REJECTED]
        #show pending requests first
        if pending:
            print(" PENDING REQUESTS:\n")
            
            for idx, req in enumerate(pending, 1):
                print(f"{idx}. {req.student.name}")
                print(f"   Subject: {req.subject}")
                print(f"   Mode: {req.mode}")
                print(f"   Message: {req.message or 'None'}")
                print(f"   Requested: {req.created_at.strftime('%Y-%m-%d %H:%M')}")
                print()
            #tutor responds to requests    
            choice = input("Enter request number to respond (or 'skip'): ").strip()
            
            if choice.lower() != 'skip':
                try:
                    req_idx = int(choice) - 1
                    if 0 <= req_idx < len(pending):
                        self.respond_to_request(pending[req_idx])
                except ValueError:
                    pass
                
        #show accepted requests        
        if accepted:
            print("\n ACCEPTED REQUESTS:\n")
            for idx, req in enumerate(accepted, 1):
                print(f"{idx}. {req.student.name}")
                print(f"   Subject: {req.subject}")
                print(f"   Mode: {req.mode}")
                print(f"   Contact: {req.student.phone} | {req.student.email}")
                print()
        #show rejected requests        
        if rejected:
            print(f"\n REJECTED REQUESTS ({len(rejected)}):\n")
            for req in rejected[:10]: #show up to 10
                print(f"- {req.student.name} ({req.subject})")
                
        input("Press Enter to continue...")
    
    #accept, reject or go back
    def respond_to_request(self, request):
        self.clear_screen()
        self.display_header()
        print(f"RESPOND TO REQUEST FROM {request.student.name}\n")
        
        print(f"Student: {request.student.name}")
        print(f"Subject: {request.subject}")
        print(f"Tutoring Mode: {request.mode}")
        print(f"Student Contact: {request.student.phone} | {request.student.email}")
        if request.message:
            print(f"Message: {request.message}")
        print("\n" + "-" * 50)
        print("1. Accept Request")
        print("2. Reject Request")
        print("3. Back")
        print("-" * 50)
        
        choice = input("Select (1-3): ").strip()
        #handle tutor's decision
        try:
            if choice == "1":
                request.accept()
                self.session.commit()
                print(f"\n Request accepted!")
                print(f"   Contact the student at:")
                print(f"   Phone: {request.student.phone}")
                print(f"   Email: {request.student.email}")
                input("Press Enter to continue...")
            
            elif choice == "2":
                request.reject()
                self.session.commit()
                print(f"\n Request rejected!")
                input("Press Enter to continue...")
            
            elif choice == "3":
                return
        
        except Exception as e:
            self.session.rollback()
            print(f" Error: {str(e)}")
            input("Press Enter to continue...")
    
    #view all students who have requested this tutor        
    def view_all_students(self):
        self.clear_screen()
        self.display_header()
        print(" LEARNERS REQUESTING MY SERVICES\n")
        #fetch all tutor requests
        requests = self.session.query(TutorRequest).filter_by(
            tutor_id=self.tutor.id
        ).all()
        
        if not requests:
            print("No students have requested you yet.")
            input("Press Enter to continue...")
            return
        
        #group requests by student to show each student
        students_dict = {}
        for req in requests:
            student_id = req.student_id
            if student_id not in students_dict:
                students_dict[student_id] = {
                    'student': req.student,
                    'requests': []
                }
            students_dict[student_id]['requests'].append(req)
        
        #display each student and summary of request statuses
        for idx, (student_id, data) in enumerate(students_dict.items(), 1):
            student = data['student']
            reqs = data['requests']
            
            #count request statuses per student
            status_counts = {}
            for req in reqs:
                status = req.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
            
            print(f"{idx}. {student.name}")
            print(f"   Location: {student.location}")
            print(f"   Phone: {student.phone}")
            print(f"   Email: {student.email}")
            print(f"   Interests: {student.subjects_of_interest}")
            print(f"   Requests: {', '.join([f'{k}({v})' for k, v in status_counts.items()])}")
            print()
            
        input("Press Enter to continue...")
        
    def view_profile(self):
        self.clear_screen()
        self.display_header()
        print(" MY PROFILE\n")
        #display tutor details
        print(f"Name: {self.tutor.name}")
        print(f"Email: {self.tutor.email}")
        print(f"Phone: {self.tutor.phone}")
        print(f"Location: {self.tutor.location}")
        print(f"Subjects: {self.tutor.subjects}")
        print(f"Qualifications: {self.tutor.qualifications}")
        print(f"Hourly Rate: KES {self.tutor.hourly_rate}")
        print(f"Tutoring Mode: {self.tutor.tutoring_mode.value}")
        print(f"Availability: {self.tutor.availability}")
        
        input("\nPress Enter to continue...")
        
    def update_profile(self):
        self.clear_screen()
        self.display_header()
        print(" UPDATE MY PROFILE\n")
        
        print("What would you like to update?")
        print("1. Subjects")
        print("2. Qualifications")
        print("3. Hourly Rate")
        print("4. Tutoring Mode")
        print("5. Availability")
        print("6. Back to Menu")
        print("-" * 50)
        
        choice = input("Select (1-6): ").strip()
        
        try:
            if choice == "1":
                new_subjects = input("New subjects (comma-separated): ").strip()
                if new_subjects:
                    self.tutor.subjects = new_subjects
                    self.session.commit()
                    print(" Subjects updated!")
            
            elif choice == "2":
                new_quals = input("New qualifications: ").strip()
                if new_quals:
                    self.tutor.qualifications = new_quals
                    self.session.commit()
                    print(" Qualifications updated!")
            
            elif choice == "3":
                try:
                    new_rate = float(input("New hourly rate (KES): ").strip())
                    if new_rate > 0:
                        self.tutor.hourly_rate = new_rate
                        self.session.commit()
                        print(" Hourly rate updated!")
                    else:
                        print(" Rate must be greater than 0!")
                except ValueError:
                    print(" Invalid rate entered!")
            
            elif choice == "4":
                print("\n1. Physical\n2. Online\n3. Both")
                
                mode_choice = input("Select (1-3): ").strip()
                mode_map = {"1": "physical", "2": "online", "3": "both"}
                #update tutoring mode
                if mode_choice in mode_map:
                    from lib.models import TutoringMode
                    self.tutor.tutoring_mode = TutoringMode[mode_map[mode_choice].upper()]
                    self.session.commit()
                    print(" Tutoring mode updated!")
            
            elif choice == "5":
                new_availability = input("New availability status (e.g., Available, Busy, On Leave): ").strip()
                if new_availability:
                    self.tutor.availability = new_availability
                    self.session.commit()
                    print(" Availability updated!")
            
            elif choice == "6":
                return
            
            input("Press Enter to continue...")
        
        except Exception as e:
            self.session.rollback()
            print(f" Error updating profile: {str(e)}")
            input("Press Enter to continue...")
            
    def delete_account(self):
        self.clear_screen()
        self.display_header()
        print(" DELETE MY ACCOUNT\n")
        
        print(" WARNING: This action is irreversible!")
        print(f"You are about to delete: {self.tutor.name} ({self.tutor.email})")
        print("\nThis will:")
        print("  -> Remove your account from the system")
        print("  -> Delete all student requests related to you")
        print("  -> You will NOT be able to recover this data")
        print("\n" + "-" * 50)
        
        confirm = input("Type 'DELETE' to confirm account deletion: ").strip()
        
        if confirm == "DELETE":
            print("\nDeleting your account...")
            try:
                #delete tutor
                self.session.delete(self.tutor)
                self.session.commit()
                
                print(" Your account has been deleted successfully.")
                print("You will be logged out now.")
                input("Press Enter to continue...")
                return True
            except Exception as e:
                self.session.rollback()
                print(f"Error deleting account: {str(e)}")
                input("Press Enter to continue...")
                return False
        else:
            print("\n Account deletion cancelled.")
            input("Press Enter to continue...")
            return False
        
    
    def logout(self):
        print("\n Logged out successfully.")
        input("Press Enter to continue...")
    #display tutor menu
    def display(self):
        self.tutor_menu()
        
        
        
        
            
        
        
        
        