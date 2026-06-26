import json
import os
from datetime import datetime, timedelta
from app.model.file_path_model import DatabaseConnectionModel

class TableManager:
    """
    Handles Restaurant Tables (Booking, Status, Persistence).
    Adapts automatically to new JSON structure (id, seats, is_free, exp, occupied).
    """
    def __init__(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(base_dir, "database", DatabaseConnectionModel.TABLE_DATA)
            
            try:
                os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            except OSError as e:
                print(f">> ⚠️ System Error: Cannot create database folder. Details: {e}")

            self.tables = self.load_tables()
            
        except Exception as e:
            print(f">> ⚠️ Critical Error: Table Manager failed to start. Details: {e}")
            self.tables = []

    def load_tables(self):
        """Tables load karo. Agar file nahi hai, to default tables create karo."""
        if not os.path.exists(self.db_path):
            return self.create_default_tables()
            
        try:
            with open(self.db_path, 'r') as file:
                data = json.load(file)
                if not data:
                    return self.create_default_tables()
                return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f">> ⚠️ File Error (Loading Default). Details: {e}")
            return self.create_default_tables()
        except Exception as e:
            print(f">> ⚠️ Unexpected Error loading tables. Details: {e}")
            return []

    def create_default_tables(self):
        """Naye JSON structure ke hisaab se default data"""
        try:
            default_data = [
                {"id": "T1", "seats": 2, "occupied": 0, "is_free": True, "exp": None},
                {"id": "T2", "seats": 2, "occupied": 0, "is_free": True, "exp": None},
                {"id": "T3", "seats": 4, "occupied": 0, "is_free": True, "exp": None},
                {"id": "T4", "seats": 4, "occupied": 0, "is_free": True, "exp": None},
                {"id": "T5", "seats": 4, "occupied": 0, "is_free": True, "exp": None},
                {"id": "T6", "seats": 6, "occupied": 0, "is_free": True, "exp": None},
                {"id": "T7", "seats": 6, "occupied": 0, "is_free": True, "exp": None},
                {"id": "T8", "seats": 8, "occupied": 0, "is_free": True, "exp": None}
            ]
            self.tables = default_data
            self.save_tables()
            return default_data
        except Exception as e:
            print(f">> ⚠️ Failed to create default tables. Details: {e}")
            return []

    def save_tables(self):
        try:
            with open(self.db_path, 'w') as file:
                json.dump(self.tables, file, indent=4)
            return True
        except Exception as e:
            print(f">> ⚠️ Error saving table data. Details: {e}")
            return False

    def refresh_table_status(self):
        """
        Check expiry and update status logic. 
        Auto-fixes old keys to new keys (seats, exp, is_free).
        """
        try:
            if not self.tables: return

            current_time = datetime.now()
            updated = False

            for table in self.tables:
                # 🛠 FIX: Data migration (Agar user ki JSON aadhi adhuri hai)
                table.setdefault('seats', 4)
                table.setdefault('occupied', 0)
                table.setdefault('is_free', True)
                table.setdefault('exp', None)

                # Check Expiry Time
                if table.get('exp'):
                    try:
                        end_time = datetime.strptime(table['exp'], "%Y-%m-%d %H:%M:%S")
                        if current_time > end_time:
                            table['occupied'] = 0
                            table['exp'] = None
                            updated = True
                    except ValueError as e:
                        print(f">> ⚠️ Date Parsing Error for Table {table.get('id')}. Resetting time. Details: {e}")
                        table['exp'] = None
                        updated = True

                # Occupied ke hisaab se is_free ko manage karo
                if table['occupied'] == 0:
                    if not table['is_free']:
                        table['is_free'] = True
                        updated = True
                else:
                    if table['is_free']:
                        table['is_free'] = False
                        updated = True

            if updated:
                self.save_tables()
                
        except Exception as e:
            print(f">> ⚠️ Error refreshing table status. Details: {e}")

    def book_table(self, table_id, seats_needed, duration_minutes=120):
        try:
            self.refresh_table_status() 
            
            if not self.tables:
                return False, "System Error: No tables loaded."

            table = next((t for t in self.tables if t['id'] == table_id), None)
            
            if not table:
                return False, "Invalid Table ID."

            available_seats = table['seats'] - table['occupied']
            
            if seats_needed > available_seats:
                return False, f"Not enough seats. Available: {available_seats}"

            table['occupied'] += seats_needed
            table['is_free'] = False
        
            expiry_time = datetime.now() + timedelta(minutes=duration_minutes)
        
            if table['exp'] is None:
                table['exp'] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")

            if self.save_tables():
                return True, f"Successfully booked {seats_needed} seats on {table_id}."
            else:
                return False, "Failed to save booking. Try again."

        except Exception as e:
            print(f">> ⚠️ Booking failed due to system error. Details: {e}")
            return False, f"System Error: {e}"

    def reset_table(self, table_id):
        """Table ko forcibly release/reset karne ke liye"""
        try:
            table = next((t for t in self.tables if t['id'] == table_id), None)
            
            if not table:
                return False, "Invalid Table ID. Not found."

            table['occupied'] = 0
            table['exp'] = None
            table['is_free'] = True

            if self.save_tables():
                return True, f"Table {table_id} is now completely FREE."
            else:
                return False, "Failed to save database after resetting table."
                
        except Exception as e:
            print(f">> ⚠️ Reset table failed. Details: {e}")
            return False, f"System Error: {e}"

    def get_all_tables(self):
        try:
            self.refresh_table_status()
            return self.tables
        except Exception as e:
            print(f">> ⚠️ Error fetching tables. Details: {e}")
            return self.tables if self.tables else []