import math
def sine_series(n,x):
    sum=0
    for i in range(n):
        sum+=((-1)**i*(x**(2^i+1)))/math.factorial(2*i+1)
        return sum
n=int(input("Enter the no of terms:"))
x=float(input("enter the value of x(in radians):"))
print("sum of sine series:",sine_series(n,x))
