class InsufficientBalanceError(Exception):
    pass
class BankAccount:
    def __init__(self,initial_balance=0):
        self.balance=initial_balance
    def deposit(self,amount):
        if amount<=0:
            raise ValueError("Deposit amount must be positive.")
        self.balance+=amount
    def withdraw(self,amount):
        if amount<=0:
            raise ValueError("Withdrawel amount must be positive.")
        if amount>self.balance:
            raise InsufficientBalanceError("Insufficient balance")
        self.balance-=amount
    def display_balance(self):
        print("Current balance:",self.balance)
account=BankAccount(1000)
try:
    account.withdraw(int(input("Withdraw amount:")))
    account.display_balance()
    account.deposit(int(input("Deposit:")))
    account.display_balance()
except InsufficientBalanceError as e:
    print(e)
except ValueError as e:
    print(e)
