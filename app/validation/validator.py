import re
import pwinput


class Validator:
    """
    Utility class handles all user input validation.
    """


    @staticmethod
    def get_valid_phone():
        while True:
            phone = input("Enter Phone Number: ").strip()
           
            clean_phone = phone.replace(" ", "").replace("-", "")
       
            if clean_phone.startswith("+91"):
                clean_phone = clean_phone[3:]
           
            if not clean_phone.isdigit() or len(clean_phone) != 10:
                print("Invalid Phone! Must be a 10-digit number.")
                continue


            if re.search(r"(.)\1{4,}", clean_phone):
                print("Invalid Phone! A digit cannot repeat more than 4 times consecutively (e.g., 99999).")
                continue
               
            return clean_phone


    @staticmethod
    def get_valid_name(prompt="Enter Name: "):
        while True:
            name = input(prompt).title().strip()
           
            if len(name) == 0:
                print("Name cannot be empty.")
                continue
           
            if not re.fullmatch(r"[A-Za-z ]+", name):
                print("Invalid Name. Only letters and spaces allowed.")
                continue
           
            if len(name) > 30:
                print("Invalid Name. Must not exceed 30 characters.")
                continue
           
            if re.search(r"(.)\1{2,}", name):
                print("Invalid Name. Characters cannot repeat more than 2 times consecutively.")
                continue
               
            return name


    @staticmethod
    def get_valid_email():
        while True:
            email = input("Enter Email: ").lower().strip()


            pattern = r"^[a-z0-9.]{3,15}@[a-z0-9]+\.[a-z]{2,}$"
            if not re.fullmatch(pattern, email):
                print("Invalid Email format. Before '@' keep 3-15 chars. Example: dev123@gmail.com")
                continue


            username = email.split("@")[0]
           
            if username.isdigit():
                print("Invalid Email! Username cannot be purely numbers (like 123@...).")
                continue
           
            # set(username) unique characters nikalta hai. Agar length 1 hai, matlab sab same hai.
            if len(set(username)) == 1:
                print("Invalid Email! Username cannot have all repeated characters (like aaa@... or 000@...).")
                continue


            return email
       


    @staticmethod
    def get_valid_address():
        while True:
            address = input("Enter Address: ").strip()
           
            if len(address) < 5:
                print("Invalid Address! It is too short (min 5 chars).")
                continue
       
            if len(address) > 40:
                print("Invalid Address! It is too long (max 40 chars).")
                continue


       
            if re.search(r"(.)\1{3,}", address):
                print("Invalid Address! Do not repeat the same character 4 or more times (e.g., hhhhh, 1111).")
                continue
               
            return address
       
       
    @staticmethod
    def get_valid_department():
        allowed_departments = ["Kitchen", "Service", "Management"]
       
        while True:
            dept_input = input("Enter Department (e.g. Kitchen, Service, Management): ").title().strip()
           
            if any(char.isdigit() for char in dept_input):
                print("Invalid! Department name cannot contain numbers.")
                continue


            if dept_input in allowed_departments:
                return dept_input
           
            print(f"Invalid Department. Please choose from: {', '.join(allowed_departments)}")


    @staticmethod
    def get_valid_experience():
        while True:
            exp_input = input("Enter Experience (Years): ").strip()
           
            if not exp_input.isdigit():
                print("Invalid! Please enter numbers only.")
                continue
           
            exp_val = int(exp_input)
           
            if exp_val >= 40:
                print("Invalid Experience. Must be less than 40 years.")
                continue
           
            return f"{exp_val} Years"
       
    @staticmethod
    def get_valid_password():
        while True:
            password = pwinput.pwinput(prompt="Enter Password (must be exactly 8 chars): ", mask="*").strip()


            if len(password) != 8:
                print("Invalid! Password must be exactly 8 characters long.")
                continue


            # Check if any character repeats 8 times
            if any(password.count(ch) == 8 for ch in set(password)):
                print("Invalid! Weak password no character can repeat 8 times (e.g., aaaaaaaa or 11111111).")
                continue


            return password


    @staticmethod
    def get_valid_numeric_choice():
        while True:
            try:
                choice_input = input(f"Enter your choice: ").strip()


                if not choice_input:
                    print("Please enter a choice.")
                    continue


                val = int(choice_input)
                if 1 <= val <= 10:
                    return val


                print(f"Invalid Choice.")
               
            except ValueError:
                print("Invalid Input! Please enter a numeric value.")
               
               
    @staticmethod
    def get_valid_Quantity():
        while True:
            try:
                choice_input = input(f"Enter Quantity: ").strip()


                if not choice_input:
                    print("Please Enter Quantity: .")
                    continue


                val = int(choice_input)
                if 1 <= val <= 100:
                    return val


                print(f"Invalid Choice.")
               
            except ValueError:
                print("Invalid Input! Please try again.")
               
    # --- PAYMENT VALIDATORS ---


    @staticmethod
    def get_valid_card_number():
        while True:
            card = input("Enter 16-digit Card Number: ").strip().replace(" ", "")
            if card.isdigit() and len(card) == 16:
                return card
            print(">> Invalid Card Number! Must be 16 digits.")


    @staticmethod
    def get_valid_cvv():
        while True:
            cvv = input("Enter 3-digit CVV: ").strip()
            if cvv.isdigit() and len(cvv) == 3:
                return int(cvv)
            print(">> Invalid CVV!")


    @staticmethod
    def get_valid_upi_id():
        while True:
            upi = input("Enter UPI ID (e.g., name@bank.ybl): ").strip()
            if "@" in upi and "." in upi:
                return upi
            print(">> Invalid UPI ID! Format: user@bank")

    @staticmethod
    def get_valid_cash_amount(bill_amount):
        total_collected = 0.0
       
        while True:
            try:
                remaining = bill_amount - total_collected
                if remaining <= 0:
                    return total_collected


                print(f"\n>> Total Bill:   ₹{bill_amount:.2f}")
                if total_collected > 0:
                    print(f">> Paid So Far:  ₹{total_collected:.2f}")
                    print(f">> Remaining:    ₹{remaining:.2f}")
               
                cash_input = float(input(f"Enter Cash Amount (Need ₹{remaining:.2f} more): ₹"))
               
                if cash_input < 0:
                    print(">> ❌ Amount cannot be negative.")
                    continue
               
                total_collected += cash_input
               
                if total_collected >= bill_amount:
                    return total_collected
               
                print(f">> ✅ Accepted ₹{cash_input:.2f}.")
               
            except ValueError:
                print(">> Invalid Amount! Enter numbers only.")
               
   
    @staticmethod
    def get_valid_offer_code_input():
        """
        Validates format of Welcome Code.
        Rule: Must be Alphanumeric and at least 6 characters long.
        """
        while True:
            code = input("Enter Welcome Code: ").strip().upper()
           
           
            if len(code) >= 6 and code.isalnum():
                return code
            print(">> Invalid Format! Code must be at least 6 characters (Letters/Numbers).")