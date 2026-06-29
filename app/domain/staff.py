import datetime
import time
from app.validation.validator import Validator
from app.menu.manager import MenuManager
from app.order.manager import OrderManager
from app.inventory.table_manager import TableManager

class StaffPanel:
    def __init__(self, user):
        self.user = user
        self.menu_mgr = MenuManager()
        self.order_mgr = OrderManager()
        self.table_mgr = TableManager()

    def dashboard(self):
        while True:
            print(f"\n===== STAFF DASHBOARD ({self.user.name}) =====")
            print("1. Manage Tables & Orders")
            print("2. Logout")
            
            choice = Validator.get_valid_numeric_choice()

            if choice == 1:
                self.handle_table_service()
            elif choice == 2:
                print(f"Bye {self.user.name}! Have a great rest.")
                break
            else:
                print("Invalid choice! Please select 1 or 2.")

    def handle_table_service(self):
        tables = self.table_mgr.get_all_tables()
        
        print("\n" + "─"*50)
        print(f"{' ':<14} RESTAURANT MAP {' ':<14}")
        print("─"*50)
        print(f"{'Table':<8} | {'Seats':<7} | {'Status'}")
        print("-" * 50)

        for t in tables:
            icon = "🟢 FREE" if t['is_free'] else "🔴 OCCUPIED"
            print(f"{t['id']:<8} | {t['seats']:<7} | {icon}")

        print("-" * 50)
        print("1. Select a Table")
        print("2. Back")
        
        c = Validator.get_valid_numeric_choice()
        if c == 2: return
        
        table_id = input("Enter Table ID (e.g., T1): ").strip().upper()
        current_table = next((t for t in tables if str(t.get('id', '')) == table_id), None) # <-- Made robust
        
        if not current_table:
            print(f">> Invalid Table ID! '{table_id}' not found.")
            return

        if current_table['is_free']:
            confirm = input(f"Book Table {table_id} for customer? (y/n): ").lower()
            if confirm == 'y':
                try:
                    # FIX: We need to ask for seats or default to the table's capacity
                    seats_needed = int(input("Enter seats required: "))
                    # FIX: table_mgr.book_table requires table_id AND seats_needed
                    success, msg = self.table_mgr.book_table(table_id, seats_needed)
                    print(f">> {msg}")
                    if success:
                        self.take_order(table_id)
                except ValueError:
                    print(">> Invalid number for seats.")
                except Exception as e:
                     print(f">> Error during booking: {e}")
        else:
            print(f"\nTable {table_id} is currently OCCUPIED.")
            print("1. Add items to order / Generate Bill")
            print("2. Back")
            act = Validator.get_valid_numeric_choice()
            if act == 1:
                self.take_order(table_id)

    def take_order(self, table_id):
        cart = []
        while True:
            print(f"\n--- ORDERING FOR TABLE: {table_id} ---")
            print("1. Show Menu & Add Item")
            print("2. View Cart")
            print("3. Proceed to Payment & Bill")
            print("4. Back")
            
            c = Validator.get_valid_numeric_choice()

            if c == 1:
                self.menu_mgr.view_menu()
                try:
                    item_id = int(input("Enter Item ID: "))
                    qty = Validator.get_valid_Quantity()
                    
                    menu_items = self.menu_mgr.get_all_items()
                    item = next((i for i in menu_items if i['id'] == item_id), None)
                    
                    if item:
                        price = item['price']
                        cart.append({"name": item['name'], "price": price, "qty": qty})
                        print(f"Added: {item['name']} x{qty} - ₹{price * qty}")
                    else:
                        print("Invalid Item ID")
                except ValueError:
                    print("Invalid Input")

            elif c == 2:
                print("\n--- Current Cart ---")
                if not cart: print("(Empty)")
                for i in cart:
                    print(f"{i['name']} x{i['qty']} - ₹{i['price'] * i['qty']}")

            elif c == 3:
                if not cart:
                    print("Cart is empty!")
                    continue
                
                subtotal = sum(item['price'] * item['qty'] for item in cart)
                total_estimated = subtotal * 1.05  # 5% GST
                
                print(f"\nBILL SUMMARY (Est.): ₹{total_estimated:.2f}")
                payment_info = self.collect_payment(total_estimated)
                
                if payment_info:
                    print("\n>> 💳 Processing Order...")
                    order = self.order_mgr.process_order(table_id, cart, self.user.uid, payment_info)
                    if order:
                        self.print_bill(order, table_id)
                        
                        rel = input(f"Release Table {table_id}? (y/n): ").lower()
                        if rel == 'y':
                            self.table_mgr.reset_table(table_id)  # <--- FIXED HERE
                            print(f"Table {table_id} is now FREE.")
                        break
                else:
                     print("\n>>  Payment Cancelled.")
            
            elif c == 4:
                break

    def collect_payment(self, amount):
        print("\n--- SELECT PAYMENT MODE ---")
        print("1. Cash 💵\n2. UPI  📱\n3. Card 💳\n4. Cancel")
        choice = Validator.get_valid_numeric_choice()
        
        payment_data = {
            "final_amount": amount,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if choice == 1:
            payment_data['mode'] = 'CASH'
            received = Validator.get_valid_cash_amount(amount)
            payment_data['received'] = received
            payment_data['change'] = received - amount
            print(">> Payment Accepted!")
            return payment_data
        elif choice == 2: 
            payment_data['mode'] = 'UPI'
            print(">> UPI Payment Received!")
            return payment_data
        elif choice == 3:
            payment_data['mode'] = 'CARD'
            print(">> Card Transaction Approved!")
            return payment_data
        return None

    def print_bill(self, order, table_id):
        print("\n" + "="*30)
        print("      BITEHUB RESTAURANT      ")
        print("="*30)
        print(f"Table: {table_id} | Staff: {self.user.name}")
        print("-" * 30)
        for item in order['items']:
            print(f"{item['name']:<15} x{item['qty']:<2} ₹{item['price']*item['qty']}")
        print("-" * 30)
        print(f"Total Paid: ₹{order['total']:.2f}")
        print("="*30 + "\n")