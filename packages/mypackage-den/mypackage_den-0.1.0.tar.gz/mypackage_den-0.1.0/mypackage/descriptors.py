# mypackage/descriptors.py
import math

class ShowAccess:
    def __get__(self, instance, owner):
        value = instance.__dict__[self.name]
        print(f"Get {self.name} = {value}")
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        print(f"Set {self.name} = {value}")

    def __delete__(self, instance):
        value = instance.__dict__.pop(self.name)
        print(f"Delete {self.name} = {value}")

    def __set_name__(self, owner, name):
        self.name = name

class Circle:
    radius = ShowAccess()
    
    def __init__(self, radius):
        self.radius = radius
    
    @property
    def area(self):
        return math.pi * self.radius ** 2

if __name__ == "__main__":
    c = Circle(100)
    print("Площадь круга:", c.area)
    del c.radius
