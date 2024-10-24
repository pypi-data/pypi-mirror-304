age=int(input("enter your age:"))
if(age>=18):
    print("you are eligible to vote")
elif(age>=13)and(age<18):
        print("you are teenagar")
elif(age>=0)and(age<13):
        print("you are a kid")
else:
        print("invalid age,please enter a validage")
