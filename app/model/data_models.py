class User:
    def __init__(self, uid, name, phone, email, password, role, address, department=None, experience=None, reward_points=0):
        self.uid = uid
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.role = role
        self.address = address
        self.department = department
        self.experience = experience

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "address": self.address,
            "department": self.department,
            "experience": self.experience,
        }


    @classmethod
    def from_dict(cls, data):
        return cls(
            uid=data["uid"],
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
            address=data["address"],
            department=data.get("department"),
            experience=data.get("experience"),
        )