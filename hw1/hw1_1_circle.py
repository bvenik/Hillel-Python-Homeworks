import math


def calculate_circle_area(radius: float) -> float | str:
    """
    Calculate the area of a circle.
    :param radius: Radius of the circle.
    :return: Area of the circle.
    """
    return round(math.pi * (radius ** 2), 2) if radius >= 0 else "Error, radius cannot be negative!" # 1st case: if radius >= 0 return area. 2nd case: if radius <0 return error text


try:
    result = calculate_circle_area(float(input("Greetings! Enter radius: ")))
    print(result) if isinstance(result, str) else print(f"Area is {result} cm^2") # 1st case: if result is str -> print result(error text). 2nd case: if result is not str (float/int) -> print result(number)

except ValueError:
    print("Error, that is not a number!")
