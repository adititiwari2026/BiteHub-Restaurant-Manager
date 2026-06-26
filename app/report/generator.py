from app.database.file_manager import FileManager
from app.model.file_path_model import DatabaseConnectionModel

class ReportGenerator:
    """
    Handles Reporting logic: Revenue and Order Stats.
    Secure & Crash-Proof.
    """
    ORDERS_FILE = DatabaseConnectionModel.ORDER_DATA

    def generate_daily_report(self):
        try:
            orders = FileManager.load_data(self.ORDERS_FILE)
            
            if not orders:
                print("\nNo orders found for today.")
                return

            total_revenue = sum(order['total'] for order in orders)
            total_orders = len(orders)
            
            item_counts = {}
            for order in orders:
                for item in order['items']:
                    name = item['name']
                    item_counts[name] = item_counts.get(name, 0) + item['qty']
            
            best_seller = max(item_counts, key=item_counts.get) if item_counts else "N/A"

            print("\n" + "="*40)
            print("       BUSINESS REPORT       ")
            print("="*40)
            print(f"Total Revenue:    ₹{total_revenue}")
            print(f"Total Orders:     {total_orders}")
            print(f"Best Selling:     {best_seller}")
            print("="*40)

        except Exception as e:
            print(">> Error generating report.")