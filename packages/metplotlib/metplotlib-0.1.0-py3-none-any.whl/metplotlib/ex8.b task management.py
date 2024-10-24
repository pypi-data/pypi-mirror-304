def add_task():
    task=input("Enter task:")
    with open("tasks.txt","a") as file:
        file.write(task+"\n")
def view_tasks():
    with open("tasks.txt","r") as file:
        print(file.read())
while True:
    print("1.Add Task")
    print("2.View Tasks")
    print("3.Exit")
    choice=input("Enter choice:")
    if choice=="1":
        add_task()
    elif choice=="2":
        view_tasks()
    elif choice=="3":
        break
    else:
        print("Invalid choice")
