class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def bark(self):
        print("bark bark")

dog1 = Dog("Buddy", 9)
print(dog1.name + " is " + str(dog1.age) + " years old")
dog2 = Dog("Max", 10)   
print(dog2.name + " is " + str(dog2.age) + " years old")

dog1.bark()
dog2.bark()



