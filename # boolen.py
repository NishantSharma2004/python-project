# boolen
"""
Evaluate Values and Variables
The bool() function allows you to evaluate any value, and give you True or False in return,
"""
#Example
#Evaluate a string and a number:

print(bool("Hello")) # output is true because of non empty string
print(bool(15))
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
class myclass():
      def __len__(self):
        return 0

myobj = myclass()
print(bool(myobj))
