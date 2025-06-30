#function are of two types
#1. Built-in functions  
#2. User-defined functions
# Built-in functions
# print() - used to display output  
# input() - used to take input from user
# len() - used to find length of a string, list, tuple, set, dictionary
# type() - used to find type of a variable
# int() - used to convert a string to integer

# User-defined functions
#def = keyword used to define a function
#function_name = name of the function
#parameters = input values for the function
#return = output value of the function

def print_hello(): #no input or output
    print("Hello, World!")
print_hello()

# arguments
def add(n1,n2):
    sum = n1+n2
    print("Sum is:", sum)
add(10, 2)  # positional arguments

#keyword arguments
def add_numbers(n1, n2):
    print("n1:",n1)
    print("n2:",n2)
    sum = n1 + n2
    print("Sum is:", sum)
    return sum

add_numbers(n2=20, n1=10)  # keyword arguments

# default arguments
def multiply(n1, n2=1):
    product = n1 * n2
    print("Product is:", product)
    return product

multiply(5)  # using default argument
multiply(5, 2)  # using both arguments

#arbitrary arguments
def add_multiple(*args):
    total = 0
    for num in args:
        total += num
    print("Total is:", total)
    return total
add_multiple(1, 2, 3, 4, 5)  # passing multiple arguments

#keyword arbitrary arguments kwargs
def student_info(**kwargs):
    for x,y in kwargs.items():
        print(x,"is",y)
student_info(name="Niku", age=20, city="Delhi")  # passing keyword arguments
student_info(name="Manoj", age=22, city="Mumbai", course="Python")  # passing more keyword arguments

#nested functions
def outer_function():
    x = 10
    def inner_function():
        y = 20
        result = x + y
        return result
    result = inner_function()
output = outer_function()
print("Output of nested function:", output)  # Output of nested function: 30

#pass by value  immutable types like int, float, str, tuple
def addone(x):
    x= x + 1
    print("Inside function, x:", x)
x = 10
addone(x)
print("Outside function, x:", x)  # Outside function, x: 10

#pass by reference original list is modified
def addone_to_list(lst):
    lst.append(1)
    print("Inside function, lst:", lst)
lst = [1, 2, 3]
addone_to_list(lst)
print("Outside function, lst:", lst)  # Outside function, lst: [1, 2, 3, 1]
#function for calculating factorial of a number
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
        
factorial(5)
print("Factorial of n is:", factorial(5))  # Factorial of 5 is: 120 