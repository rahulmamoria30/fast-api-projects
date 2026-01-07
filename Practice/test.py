# thislist = ["apple", "banana", "cherry"]
# thislist[1:2] = ["blackcurrant", "watermelon"]
# print(thislist)
# print(len(thislist))

thislist = ["apple", "banana", "cherry"]
thislist[1:3] = ["watermelon"]
# print(thislist)

thislist.insert(1, "blackcurrant")
# print(thislist)

thislist.append("orange")
# print(thislist)

tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
# print(thislist)

thislist.remove("mango")
thislist.pop(1)
# thislist.clear()

# for x in thislist:
#     print(x)

# for i in range(len(thislist)):
#     print(thislist[i])

# i=0
# while i < len(thislist):
#     print(thislist[i])
#     i+=1

# [print(x) for x in thislist]

# if "apple" in thislist:
#     print("Yes, 'apple' is in the fruits list")


# fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
# newlist = []

# for x in fruits:
#     if "a" in x:
#       newlist.append(x)
# print(newlist)

# newList = [x for x in fruits if "a" in x]
# newlist = [x.upper() for x in fruits]
# print(newlist)

# print(fruits.sort(reverse=True))

# numbers = [100, 50, 65, 82, 23]
# numbers.sort(reverse=True)
# print(numbers)

def myfunc(n):
  return abs(n - 50)

numbers = [100, 50, 65, 82, 23]
# numbers.sort(key = myfunc)
# print(numbers)


# number2 = list(numbers)
# number2 = numbers.copy()
# number2 = numbers[:]
# print(number2)

list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list3 = list1 + list2
# print(list3)


# Tuple 
thistuple = ("apple", "banana", "cherry")
# print(len(thistuple))

# print(type(thistuple))

# the description of tuple is a collection 
# which is ordered and unchangeable.
# In Python tuples are written with round brackets.

newtuple = tuple(("apple", "banana", "cherry"))
# print(newtuple)


class Computer:
    def __init__(self, brand, model, year):
        print("Initializing Computer object...")
        self.brand=brand
        self.model=model
        self.year=year

    def description(self):
        return f"{self.year} {self.brand} {self.model}"
    
    def computer_age(self, current_year):
        print("Calculating computer age...")
        return current_year - self.year

my_computer = Computer("Dell", "XPS 13", 2020)

# print(my_computer.description())
# print(f"My computer is {my_computer.computer_age(2024)} years old.")