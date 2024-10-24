question=[("what is the capital of india?","delhi"),("what is the largest planet?","jupiter"),("what is the smallest country in the world","vatican city")]
for question,answer in question:
    user_answer=input(question+" ")
    if user_answer.lower()==answer.lower():
      print("correct!")
    else:
      print("sorry,the correct answer is",answer)
