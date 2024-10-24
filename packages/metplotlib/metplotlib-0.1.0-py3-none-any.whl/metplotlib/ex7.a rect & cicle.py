import math
class Rectangle:
    def __init__(self,length,breadth):
        self.length=length
        self.breadth=breadth
    def area(self):
        return self.length*self.breadth
class Circle:
    def __init__(self,radius):
        self.radius=radius
    def area(self):
        return math.pi*(self.radius**2)
def compute_area(shape):
    return shape.area()
rectangle=Rectangle(4,5)
circle=Circle(3)
print("Rectangle area:",compute_area(rectangle),"sq units")
print("Circle area:",compute_area(circle),"cm^2")
