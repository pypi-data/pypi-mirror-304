def addition(n1,n2):
    return n1+n2
def subtraction(n1,n2):
    return n1-n2
def multiplication(n1,n2):
    return n1*n2
def division(n1,n2):
    return n1/n2
print("select operations")
print("1.addition \n",
      "2.subtraction\n",
      "3.multiplication\n",
      "4.division\n")
operation=int(input("enter choice of operation 1\2\3\4:"))
n1=float(input("enter the first number:"))
n2=float(input("enter the second number:"))
if operation==1:
    print(n1,"+",n2,"=",addition(n1,n2))
elif operation==2:
    print(n1,"-",n2,"=",subtraction(n1,n2))
elif operation==3:
    print(n1,"*",n2,"=",multiplication(n1,n2))
elif operation==4:
    print(n1,"/",n2,"=",division(n1,n2))
else:
    print("invalid input")
    
