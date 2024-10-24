binary=int(input("enter a binary number:"))
decimal=0
power=0
while binary>0:
    last_digit=binary%10
    decimal+=last_digit*(2**power)
    binary//=10
    power+=1
print(f"decimal equivalent:{decimal}")
decimal=int(input("enter a decimal number:"))
binary=""
while decimal>0:
    binary=str(decimal%2)+binary
    decimal//=2
print(f"binary equivalent:{binary}")
