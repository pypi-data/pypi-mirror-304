class Student:
    def __init__(self, Rollno, Name, Department):
        self.Rollno = Rollno
        self.Name = Name
        self.Department = Department
    def Getvalue(self):
        self.Rollno = input("Enter Rollno: ")
        self.Name = input("Enter Name: ")
        self.Department = input("Enter Department: ")
    def Printvalue(self):
        print("Rollno: ", self.Rollno)
        print("Name:", self.Name)
        print(f"Department:", self.Department)
stu1 = Student(None, None, None)
stu2 = Student(None, None, None)
stu1.Getvalue()
print("Values of stu1:")
stu1.Printvalue()
print("Values of stu2 (no input, default values):")
stu2.Printvalue()
