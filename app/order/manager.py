import datetime
import random
from app.database.file_manager import FileManager
from app.inventory.manager import InventoryManager
from app.model.file_path_model import DatabaseConnectionModel

class OrderManager:
    """
    Handles Order Placement and Billing.
    Delegates inventory management to InventoryManager.
    Simplified version without external logging.
    """
    ORDERS_FILE = DatabaseConnectionModel.ORDER_DATA

    def __init__(self):
        try:
            self.inv_mgr = InventoryManager()
        except Exception as e:
            print(f" Error initializing Order Manager: {e}")

    def process_order(self, seat_id, cart, staff_id, payment_details):
        """
        1. Checks Inventory (via InventoryManager)
        2. Deducts Stock (via InventoryManager)
        3. Calculates Bill (GST)
        4. Saves Order with Payment Info
        """
        try:
            # 1 & 2. Check and Deduct Inventory
            if not self.inv_mgr.check_stock(cart):
                print(" Order Cancelled due to insufficient stock.")
                return None

            if not self.inv_mgr.deduct_stock(cart):
                print("Failed to update inventory. Order cancelled.")
                return None
            
            # 3. Calculate Bill
            subtotal = sum(item['price'] * item['qty'] for item in cart)
            gst_amount = subtotal * 0.05  # 5% GST
            total_amount = subtotal + gst_amount

            order_id = f"ORD{random.randint(10000, 99999)}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_order = {
                "order_id": order_id,
                "seat_id": seat_id,
                "staff_id": staff_id,
                "timestamp": timestamp,
                "items": cart,
                "subtotal": subtotal,
                "gst": gst_amount,
                "total": total_amount,
                "status": "COMPLETED",
                "payment": payment_details
            }
            
            # 4. Save Order
            orders = FileManager.load_data(self.ORDERS_FILE)
            orders.append(new_order)
            
            if FileManager.save_data(self.ORDERS_FILE, orders):
                return new_order
            else:
                print(" Error saving order record.")
                return None

        except Exception as e:
            # Standard print instead of AppLogger
            print(f" System Error: Could not process order. Details: {e}")
            return None