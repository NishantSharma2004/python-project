a = int(input("Enter a number: "))
b = int(input("Enter another number: "))
try:
    result = a / b
except ZeroDivisionError:
    result = None
    print("Error: Division by zero is not allowed.")
finally:
    print("The result is:", result)