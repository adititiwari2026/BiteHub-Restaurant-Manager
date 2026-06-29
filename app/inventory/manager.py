from app.database.file_manager import FileManager
from app.validation.validator import Validator
from app.model.file_path_model import DatabaseConnectionModel

class InventoryManager:
        """
        Handles Inventory Logic (View Stock, Add Stock, Low Stock Alerts).
        Simplified version without external logging.
        """
        INVENTORY_FILE = DatabaseConnectionModel.INVENTORY_DATA


        def view_inventory(self):
            try:
                data = FileManager.load_data(self.INVENTORY_FILE)
                if not data:
                    print("\nInventory is empty.")
                    return

                print("\n--- CURRENT INVENTORY ---")
                print(f"{'Item Name':<30} {'Quantity':<10} {'Status'}")
                print("-" * 55)
          
                for item in data:
                    qty = item['quantity']
                    status = "🟢 OK" if qty >= 10 else "🟡 LOW" if qty >= 5 else "🔴 CRITICAL"
                    print(f"{item['item_name']:<30} {qty:<10} {status}")
            
            except Exception as e:
                print(f">> Error loading inventory: {e}")

        def add_stock(self):
            print("\n--- [+] ADD STOCK ---")
            try:
                self.view_inventory()
                
                item_name = Validator.get_valid_name()
                
                data = FileManager.load_data(self.INVENTORY_FILE)
                found = False
                
                for item in data:
                    if item['item_name'].lower() == item_name.lower():
                        found = True
                        print(f"Current Quantity: {item['quantity']}")
                        
                        try:
                            qty_to_add = int(input("Enter Quantity to Add: "))
                            if qty_to_add <= 0:
                                print("Quantity must be positive.")
                                return
                            
                            item['quantity'] += qty_to_add
                            
                            if FileManager.save_data(self.INVENTORY_FILE, data):
                                print(f" Stock Updated! New Quantity: {item['quantity']}")
                            else:
                                print(" Failed to save data.")
                                
                        except ValueError:
                            print("Invalid number.")
                        break
                
                if not found:
                    print(" Item not found in inventory.")

            except Exception as e:
                print(f"\n>>  System Error: Could not add stock. Details: {e}")

        def low_stock_alert(self):
            print("\n--- [!] LOW STOCK ALERTS ---")
            try:
                data = FileManager.load_data(self.INVENTORY_FILE)
                low_items = [item for item in data if item['quantity'] < 5]
                
                if not low_items:
                    print("All items are sufficient.")
                else:
                    print(f"[!] WARNING: The following items are below 5 units:")
                    for item in low_items:
                        print(f" - {item['item_name']} (Qty: {item['quantity']})")
            
            except Exception as e:
                print(f">>  Error checking low stock: {e}")

        def check_stock(self, cart):
            """
            Checks if enough stock is available for all items in the cart.
            Handles cleaning of item names (removing '(Full)' or '(Half)') for matching.
            """
            try:
                inventory_data = FileManager.load_data(self.INVENTORY_FILE)
                
                for cart_item in cart:
                    item_found = False
                    
                    search_name = cart_item['name'].replace(" (Full)", "").replace(" (Half)", "").strip()
                    
                    for stock_item in inventory_data:
                        if stock_item['item_name'] == search_name:
                            item_found = True
                            if stock_item['quantity'] < cart_item['qty']:
                                print(f"Not enough stock for {cart_item['name']}! (Available: {stock_item['quantity']})")
                                return False
                            break
                    
                    if not item_found:
                        print(f" Error: Item '{cart_item['name']}' (searched as '{search_name}') not found in inventory list.")
                        return False
                        
                return True

            except Exception as e:
                print(f" Error checking stock availability: {e}")
                return False

        def deduct_stock(self, cart):
            """
            Deducts the quantity from inventory for items in the cart.
            Handles cleaning of item names.
            """
            try:
                inventory_data = FileManager.load_data(self.INVENTORY_FILE)
                
                for cart_item in cart:
                    search_name = cart_item['name'].replace(" (Full)", "").replace(" (Half)", "").replace(" ((2 pcs))", "").replace(" (300ml)", "").replace(" (500ml)", "").replace(" (1L)", "").strip()
                    
                    for stock_item in inventory_data:
                        if stock_item['item_name'] == search_name:
                            stock_item['quantity'] -= cart_item['qty']
                            
                            if stock_item['quantity'] < 5:
                                print(f" Alert: {stock_item['item_name']} is running low (Qty: {stock_item['quantity']})")
                            break
                
                FileManager.save_data(self.INVENTORY_FILE, inventory_data)
                return True
                
            except Exception as e:
                print(f"  Error updating inventory after order: {e}")
                return False

                