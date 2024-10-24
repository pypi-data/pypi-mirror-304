class Person:
    def __init__(self,name):
        self.name=name
    def get_info(self):
        return self.name
class Student(Person):
    def __init__(self,name,student_id):
        super().__init__(name)
        self.student_id=student_id
    def get_info(self):
        return f"{self.name},Student ID:{self.student_id}"
class Teacher(Person):
    def __init__(self,name,subject):
        super().__init__(name)
        self.subject=subject
    def get_info(self):
        return f"{self.name},Subject:{self.subject}"
person=Person("John")
student=Student("Alice","S123")
teacher=Teacher("Bob","Mathematics")
print(person.get_info())
print(student.get_info())
print(teacher.get_info())
