def addition(x,y):
    return x+y
def subtraction(x,y):
    return x-y
def multiplication(x,y):
    return x*y
def division(x,y):
    if y==0:
        return "Error:Division by zero is not allowed"
    else:
        return x/y
def modulus(x,y):
    if y==0:
        return "Error:Division by zero is not allowed"
    else:
        return x%y
def exponent(x,y):
    return x**y
print("CALCULATOR")
print("1.ADD")
print("2.SUB")
print("3.MULTIPLY")
print("4.DIVISION")

print("5.MODULUs")
print("6.EXPONENT")
num1=float(input("Enter 1st num:"))
num2=float(input("Enter 2nd num:"))
choice=int(input("Enter our choice(1-6):"))
if choice==1:
    print("Addition:", addition(num1,num2))
elif choice==2:
    print("Subtraction:",subtraction(num1,num2))
elif choice==3:
    print("Multiplication:",multiplication(num1,num2))
elif choice==4:
    print("Division:",division(num1,num2))
elif choice==5:
    print("Modulus:",modulus(num1,num2))
elif choice==6:
    print("Exponent:",exponent(num1,num2))
else:
    print("Invalid Choice")
