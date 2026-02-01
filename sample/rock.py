
import random

computer = random.choice(['rock', 'paper', 'scissors'])

user = input("will you play rock paper scissors ?\n")

if user == computer:
    print("tie")
elif user == 'rock' and computer == 'paper':
    print("User win and computer choice was "+ computer)
elif user == 'scissors' and computer == 'paper':
    print("User win and computer choice was "+ computer)
elif user == 'rock' and computer == 'scissors':
    print("User win and computer choice was "+ computer)
else:
    print("you lose and computer choise was "+ computer)