num=int(input("enter a number:"))
sum_of_digits=0
while num>0:
    digit=num%10
    sum_of_digits+=digit
    num=num//10
print("sum of the digits:",sum_of_digits)
