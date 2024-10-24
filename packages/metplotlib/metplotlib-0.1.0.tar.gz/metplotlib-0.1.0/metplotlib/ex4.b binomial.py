import math
x=int(input("enter a value for x:"))
y=int(input("enter a value for y:"))
if y==1 or y==x:
    print(1)
if y>>x:
    print(0)
else:
    a=math.factorial(x)
    b=math.factorial(y)
    div=a//(b*(x-y))
    print(div)
