# multiple inheritance
class A:
    varA = "welcome to class A"
    
class B:
    varB = "welcome to class B"

class C(A,B):
    varC = "welcome to class C"

c1 = C()

print(c1.varC)
print(c1.varB)
print(c1.varA)

# Super method
# super() method is used to access mmethod of the parent class
class Car:
    def __init__(self,type):
        self.type=type
    @staticmethod
    def start():
        print ("car started..")
    @staticmethod
    def stop():
        print ("car stopped.")
class ToyotaCar(Car):
    def __init__(self,name,type):
        self.name = name
        super().__init__(type)
        super().start()
car1 = ToyotaCar("prius","electric")
print(car1.type)
print(car1.name)
