def create_student_file(filename,n):
    with open(filename,'w') as f:
        for i in range(n):
            name=input("Enter Name:")
            regno=input("Enter Reg.No:")
            dob=input("Enter DOB:")
            branch=input("Enter Branch:")
            grade=input("Enter Grade:")
            f.write(f"{name},{regno},{dob},{branch},{grade}\n")
def read_student_file(filename):
    with open(filename,'r') as f:
        for line in f:
            name,regno,dob,branch,grade=line.strip().split(',')
            print(f"Name:{name},Reg No:{regno},DOB:{dob},Branch:{branch},Grade:{grade}")
filename="student.txt"
n=int(input("Enter number of students:"))
create_student_file(filename,n)
read_student_file(filename)
