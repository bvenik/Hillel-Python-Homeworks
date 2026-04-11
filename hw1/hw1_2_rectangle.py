class Rectangle:
    """
    Rectangle class with own width and height. Supports some operations.
    """

    def __init__(self, width: float, height: float):
        """
        Rectangles sides initialization
        """
        self.width = width
        self.height = height

    def area(self):
        """
        Finds & returns the area of the rectangle.
        """
        return self.width * self.height

    def perimeter(self):
        """
        Finds & returns the perimetr of the rectangle.
        """
        return (self.width + self.height) * 2

    def is_square(self):
        """
        Checks if the rectangle is square. (Both sides equal)
        """
        return self.width == self.height

    def resize(self, new_width: float, new_height: float):
        """
        Resizes(changes) old rectangle's width & height with new ones.
        """
        self.width = new_width
        self.height = new_height



rec = Rectangle(100, 200)
print(rec.width, rec.height)
print(rec.area())
print(rec.perimeter())
print(rec.is_square())
print("-" * 30)
rec.resize(30, 30)
print(rec.width, rec.height)
print(rec.area())
print(rec.perimeter())
print(rec.is_square())
