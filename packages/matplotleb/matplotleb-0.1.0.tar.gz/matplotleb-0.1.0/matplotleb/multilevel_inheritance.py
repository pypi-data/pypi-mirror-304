class Student:
    def __init__(self, Rollno=None, Name=None, Department=None):
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
        print("Department:", self.Department)

class Master:
    def __init__(self):
        self.Student = Student()
        self.Sports = None
        self.OnlineCourse = None
    def Getvalue(self):
        self.Student.Getvalue()
        self.Sports = input("Enter Sports: ")
        self.OnlineCourse = input("Enter Online Course: ")
    def Printvalue(self):
        self.Student.Printvalue()
        print("Sports:", self.Sports)
        print("Online Course:", self.OnlineCourse)

class Extra_curricular(Master):
    def __init__(self):
        self.Master=Master()
        self.Hobby=None

    def Getvalue(self):
        self.Master.Getvalue()
        self.Hobby=input("Enter Hobby:")
    def Printvalue(self):
        self.Master.Printvalue()
        print("Hobby:",self.Hobby)

z=Extra_curricular()
z.Getvalue()
z.Printvalue()
