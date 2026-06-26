class DatabaseConnectionModel:
    """
    Centralized configuration for all Data File names.
    Use this class to avoid hardcoding filenames in managers.
    """
   
    USER_DATA = "users.json"
    MENU_DATA = "menu.json"
    INVENTORY_DATA = "inventory.json"
    TABLE_DATA = "tables.json"
    ORDER_DATA = "orders.json"
    FEEDBACK_DATA = "feedback.json"
    ERROR_LOGS = "error_logs.txt"