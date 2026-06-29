from app.model.role_master import RoleMaster
from app.auth.service import AuthService
from app.validation.validator import Validator
from app.menu.all_menu import MenuDisplay
from app.domain.staff import StaffPanel
from app.domain.admin import AdminPanel

class Dashboard:
    """
    Main Entry Point for the Application. 
    Handles User Authentication and Panel Redirection.
    """
    
    def __init__(self):
        try:
            self.auth_service = AuthService()
        except Exception as e:
            print(">> Critical Error: Auth Service Failed.")

    def run(self):
        """
        Runs the main application loop.
        """
        while True:
            try:
                MenuDisplay.display_main_menu()

                choice = Validator.get_valid_numeric_choice()

                if choice == 1:
                    self.auth_service.signup()
                
                elif choice == 2:
                    self.handle_login()

                elif choice == 3:
                    print("Exiting... Thank you for using Anand Casa Restro!")
                    break
                
                else:
                    print("Invalid Choice! Please select a valid option.")

            except Exception as e:
                
                print(f"System Crash Error: {e}") 
                print("An unexpected error occurred. Restarting Dashboard...")

    def handle_login(self):
        """
        Handles Login Logic and Redirects to appropriate Panel.
        """
        try:
            user = self.auth_service.login()
            
            if user:
                if user.role == RoleMaster.ADMIN:
                    try:
                        admin_panel = AdminPanel(user)
                        admin_panel.dashboard()
                    except Exception as e:
                        print(">> Working on Admin Panel.")

                elif user.role == RoleMaster.STAFF:
                    try:
                        staff_panel = StaffPanel(user)
                        staff_panel.dashboard()
                    except Exception as e:
                        print(f">> Failed to load Staff Panel. Error: {e}")

                else:
                    print(f">> Unknown Role: {user.role}. Contact System Admin.")
                    
        except Exception as e:
            print(">> Login Process Failed.")