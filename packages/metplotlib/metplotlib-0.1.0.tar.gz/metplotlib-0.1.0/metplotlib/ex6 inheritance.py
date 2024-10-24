class Employee:
    def __init__(self,name,age,employee_id):
        self.name=name
        self.age=age
        self.employee_id=employee_id
    def display_info(self):
        print(f"Name:{self.name}")
        print(f"Age:{self.age}")
        print(f"Employee ID:{self.employee_id}")
class Teaching(Employee):
    def __init__(self,name,age,employee_id,subject):
        super().__init__(name,age,employee_id)
        self.subject=subject
    def display_info(self):
        super().display_info()
        print(f"Subject:{self.subject}")
class NonTeaching(Employee):
    def __init__(self,name,age,employee_id,department):
        super().__init__(name,age,employee_id)
        self.department=department
    def display_info(self):
        super().display_info()
        print(f"Department:{self.department}")
teacher=Teaching("Alice",35,"T123","Mathematics")
non_teacher=NonTeaching("Bob",40,"NT456","Administration")
print("Teaching Staff Info:")
teacher.display_info()
print("\nNon_Teaching Staff Info:")
non_teacher.display_info()
            
