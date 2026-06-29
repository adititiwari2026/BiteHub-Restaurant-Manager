from app.validation.validator import Validator
from app.menu.manager import MenuManager
from app.inventory.manager import InventoryManager
from app.order.manager import OrderManager       
from app.report.generator import ReportGenerator
from app.inventory.table_manager import TableManager

class AdminPanel:
    def __init__(self, admin_user):
        self.admin_user = admin_user
        self.menu_mgr = MenuManager()
        self.inv_mgr = InventoryManager()
        self.order_mgr = OrderManager()
        self.report_gen = ReportGenerator()
        self.table_mgr = TableManager()

    def dashboard(self):
        while True:
            try:
                print(f"\n===== ADMIN DASHBOARD ({self.admin_user.name}) =====")
                print("1. Table Management")
                print("2. Food Menu Management")
                print("3. Inventory Management")
                print("4. Reports")
                print("5. Logout")
                
                choice = Validator.get_valid_numeric_choice()

                if choice == 1:
                    self.handle_table_management()
                elif choice == 2:
                    self.handle_menu_management()
                elif choice == 3:
                    self.handle_inventory_management()
                elif choice == 4:
                    self.handle_reports()
                elif choice == 5:
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice! Please select a valid option.")
            except Exception as e:
                print(f"\n>> ⚠️ Dashboard Error: {e}")

    def handle_table_management(self):
        while True:
            try:
                tables = self.table_mgr.get_all_tables()

                print("\n" + "─"*60)
                print(f"{' ':<18} RESTAURANT TABLE STATUS {' ':<18}")
                print("─"*60)
                print(f"{'Table':<8} | {'Seats':<7} | {'Booked':<8} | {'Free':<6} | {'Status'}")
                print("-" * 60)

                if not tables:
                    print("No tables available or error loading tables.")
                else:
                    for t in tables:
                        t_id = t.get('id', 'N/A')
                        cap = t.get('seats', 0)
                        occ = t.get('occupied', 0)
                        free = cap - occ
                        
                        if occ == 0:
                            status_display = "🟢 Free"
                        elif occ < cap:
                            status_display = "🟡 Partial"
                        elif occ >= cap:
                            status_display = "🔴 Full"
                        else:
                            status_display = "⚪ Unknown"

                print(f"{t_id:<8} | {cap:<7} | {occ:<8} | {free:<6} | {status_display}")

                print("-" * 60)
                print("\n1. Book a Table")
                print("2. Release/Reset a Table")
                print("3. Back")

                choice = Validator.get_valid_numeric_choice()

                if choice == 3:
                    break
                elif choice == 1:
                    t_id = input("Enter Table ID (e.g., T1): ").strip().upper()
                    try:
                        seats = int(input("Seats required: "))
                        success, msg = self.table_mgr.book_table(t_id, seats, duration_minutes=45)
                        print(f"\n>> {msg}")
                    except ValueError:
                        print(">> ⚠️ Error: Please enter a valid number for seats.")
                    except Exception as e:
                        print(f">> ⚠️ Unexpected Error while booking: {e}")
                        
                elif choice == 2:
                    t_id = input("Enter Table ID to Reset (e.g., T1): ").strip().upper()
                    try:
                        success, msg = self.table_mgr.reset_table(t_id)
                        print(f"\n>> {msg}")
                    except Exception as e:
                        print(f">> ⚠️ Unexpected Error while resetting: {e}")
                else:
                    print("Invalid choice! Please select 1, 2, or 3.")

            except Exception as e:
                print(f"\n>> ⚠️ Table Management System Error. Details: {e}")
                break 

    def handle_reports(self):
        while True:
            try:
                print("\n--- REPORTS ---")
                print("1. View Business Report (Revenue)")
                print("2. Back")
                
                choice = Validator.get_valid_numeric_choice()

                if choice == 1:
                    self.report_gen.generate_daily_report()
                elif choice == 2:
                    break
                else:
                    print("Invalid choice! Please select 1 or 2.")
            except Exception as e:
                print(f"\n>> ⚠️ Reports Error: {e}")

    def handle_menu_management(self):
        while True:
            try:
                print("\n--- FOOD MENU MANAGEMENT ---")
                print("1. Add Food Item")
                print("2. Remove Food Item")
                print("3. View Menu")
                print("4. Back to Dashboard")
                
                choice = Validator.get_valid_numeric_choice()
                
                if choice == 1: 
                    # 🛠️ FIX: Removed self.admin_user parameter
                    self.menu_mgr.add_food_item()
                elif choice == 2: 
                    self.menu_mgr.remove_food_item()
                elif choice == 3: 
                    self.menu_mgr.view_menu()
                elif choice == 4: 
                    break
                else:
                    print("Invalid choice! Please select 1, 2, 3, or 4.")
            except Exception as e:
                print(f"\n>> ⚠️ Menu Management Error: {e}")

    def handle_inventory_management(self):
        while True:
            try:
                print("\n--- INVENTORY MANAGEMENT ---")
                print("1. View Inventory")
                print("2. Add Stock")
                print("3. Back to Dashboard")
                
                choice = Validator.get_valid_numeric_choice()
                
                if choice == 1: 
                    self.inv_mgr.view_inventory()
                elif choice == 2: 
                    self.inv_mgr.add_stock()
                elif choice == 3: 
                    break
                else:
                    print("Invalid choice! Please select 1, 2, or 3.")
            except Exception as e:
                print(f"\n>> ⚠️ Inventory Management Error: {e}")