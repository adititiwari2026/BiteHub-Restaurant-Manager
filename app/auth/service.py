import random
from app.database.file_manager import FileManager
from app.model.data_models import User
from app.validation.validator import Validator
from app.model.file_path_model import DatabaseConnectionModel

class AuthService:
    """
    Service class responsible for handling User Authentication.
    Manages new staff registration (signup) and user authentication (login).
    Interacts directly with the FileManager for database operations.
    """

    def signup(self):
        """
        Handles the registration process for new staff members.
        Collects user data, validates it, generates a unique Staff ID, 
        and saves the record to the database.
        """
        print("\n----- STAFF SIGNUP -----")
        
        try:
            name = Validator.get_valid_name()
            phone = Validator.get_valid_phone()
            email = Validator.get_valid_email()
            
            users_data = FileManager.load_data(DatabaseConnectionModel.USER_DATA)
            
            # Check if email is already registered
            for user in users_data:
                if user['email'] == email:
                    print("This Email is already registered! Please Login.")
                    return

            password = Validator.get_valid_password()
            address = Validator.get_valid_address()
            department = Validator.get_valid_department()
            experience = Validator.get_valid_experience()

            # Generate unique Staff ID
            unique_id = f"STAFF{random.randint(1000, 9999)}"
            role = "staff"
            
            new_user = User(
                uid=unique_id,
                name=name,
                phone=phone,
                email=email,
                password=password,
                role=role,
                address=address,
                department=department,
                experience=experience
            )

            users_data.append(new_user.to_dict())
            
            if FileManager.save_data(DatabaseConnectionModel.USER_DATA, users_data):
                print(f"Signup Successful! Welcome {name}.")
                print(f"Your Staff ID is: {unique_id}")
            else:
                print("Error saving data. Please try again.")

        except Exception as e:
            # Logger removed, showing error directly in console
            print(f" System Error during Signup. Details: {e}")

    def login(self):
        """
        Handles the login process for existing users.
        Validates credentials against the saved user data and returns the User object if successful.
        """
        print("\n===== LOGIN =====")
        
        try:
            email = Validator.get_valid_email()
            password = Validator.get_valid_password()
    
            users_data = FileManager.load_data(DatabaseConnectionModel.USER_DATA)
            
            users = []
            for user_dict in users_data:
                user_obj = User.from_dict(user_dict)
                users.append(user_obj)
            
            for user in users:
                if user.email == email and user.password == password:
                    print(f"Login Successful! Welcome {user.name} ({user.role})")
                    return user
                
            print("Invalid Email or Password!")
            return None

        except Exception as e:
            print(f" Login Service Unavailable. Details: {e}")
            return None