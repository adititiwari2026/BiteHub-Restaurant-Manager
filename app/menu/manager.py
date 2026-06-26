from app.database.file_manager import FileManager
from app.model.file_path_model import DatabaseConnectionModel

class MenuManager:
    """
    Lite Menu Manager - Handles Premium Food Menu.
    No logs, no colors, strictly category-based.
    """
    MENU_FILE = DatabaseConnectionModel.MENU_DATA
    
    def get_all_items(self):
        try:
            return FileManager.load_data(self.MENU_FILE)
        except Exception:
            return []

    def add_food_item(self):
        print("--- ADD NEW FOOD ITEM ---")
        try:
            name = input("Enter Food Name: ").strip()
            
            while True:
                try:
                    price = float(input("Enter Price: "))
                    if price > 0: break
                    print("Price must be greater than 0.")
                except ValueError:
                    print("Invalid Price. Enter a number.")

            category = input("Enter Category (Appetizers/Main Course/Sides/Desserts & Beverages/Combos): ").title().strip()
            has_portion = input("Has portion options (half/full)? (y/n): ").lower() == 'y'

            menu_data = FileManager.load_data(self.MENU_FILE)
            if not menu_data: menu_data = []

            new_id = max([item['id'] for item in menu_data], default=0) + 1

            new_item = {
                "id": new_id,
                "name": name,
                "price": price,
                "category": category,
                "has_portion": has_portion,
                "is_available": True
            }
            menu_data.append(new_item)

            if FileManager.save_data(self.MENU_FILE, menu_data):
                print(f"Item '{name}' added successfully! (ID: {new_id})")
            else:
                print(" Error saving item.")

        except Exception:
            print(" Failed to add item.")

    def remove_food_item(self):
        print("\n--- REMOVE FOOD ITEM ---")
        try:
            self.view_menu()
            item_id = int(input("\nEnter Item ID to remove: "))
            
            menu_data = FileManager.load_data(self.MENU_FILE)
            if not menu_data: menu_data = []
            
            new_menu_data = [item for item in menu_data if item['id'] != item_id]

            if len(new_menu_data) < len(menu_data):
                FileManager.save_data(self.MENU_FILE, new_menu_data)
                print(f"Item {item_id} removed successfully.")
            else:
                print("Item ID not found.")

        except ValueError:
            print("Invalid ID!")
        except Exception:
            print("\n Failed to remove item.")

    def view_menu(self):
        try:
            menu_data = FileManager.load_data(self.MENU_FILE)
            if not menu_data:
                print("\nMenu is empty.")
                return

            print("\n" + "="*65)
            print("                BITEHUB RESTAURANT - PREMIUM MENU                 ")
            print("="*65)

            categories = {}
            for item in menu_data:
                cat = item.get('category', 'Others')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(item)

            for cat, items in categories.items():
                print(f"\n🔹 {cat.upper()}")
                print("-" * 65)
                print(f"{'ID':<4} | {'Name':<32} | {'Price':<8} | {'Portion'}")
                print("-" * 65)
                for item in items:
                    portion = "Half/Full" if item.get('has_portion') else "Regular"
                    print(f"{item['id']:<4} | {item['name']:<32} | ₹{item['price']:<7} | {portion}")
            print("="*65 + "\n")

        except Exception:
            print(" Cannot display menu at the moment.")

