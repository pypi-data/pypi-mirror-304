num=int(input("enter a number:"))
reverse_num=0
while num>0:
    remainder=num%10
    reverse_num=(reverse_num*10)+remainder
    num=num//10
print("reverse of the number:",reverse_num)
