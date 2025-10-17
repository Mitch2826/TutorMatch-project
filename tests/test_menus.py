"""
Test Menu Classes
File: test_menus.py
"""

print("Testing Menu Classes...")
print("-" * 50)

try:
    from lib.cli.student_menu import StudentMenu
    from lib.cli.tutor_menu import TutorMenu
    
    print("✅ StudentMenu imported successfully!")
    print("✅ TutorMenu imported successfully!")
    
    print("\n" + "-" * 50)
    print("✅ All menu classes ready to use!")
    print("-" * 50)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()