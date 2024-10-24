from dataclasses import dataclass
from typing import Tuple
import math


@dataclass
class Point:
    """
    Represents a point in a 2D plane.

    Attributes:
    - x (float): The x-coordinate of the point.
    - y (float): The y-coordinate of the point.

    Methods:
    - get_zero_distance() -> float: Returns the distance of the point from the origin (0, 0).
    - get_distance_from(point: 'Point') -> float: Returns the distance between this point and another point.
    """
    x: float
    y: float

    def get_zero_distance(self) -> float:
        """
        Computes the Euclidean distance of the point from the origin (0, 0).

        Returns:
        - float: The distance from the origin.
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def get_distance_from(self, point: 'Point') -> float:
        """
        Computes the Euclidean distance between this point and another point.

        Parameters:
        - point (Point): The other point to calculate the distance from.

        Returns:
        - float: The distance between the two points.
        """
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5


@dataclass
class Triangle:
    """
    Represents a triangle in a 2D plane defined by three points.

    Attributes:
    - a (Point): The first vertex of the triangle.
    - b (Point): The second vertex of the triangle.
    - c (Point): The third vertex of the triangle.

    Methods:
    - get_area() -> float: Returns the area of the triangle.
    - get_length_side() -> Tuple[float, float, float]: Returns the lengths of the sides of the triangle.
    - is_right_triangle() -> bool: Checks if the triangle is a right-angled triangle.
    - is_triangle(a: Point, b: Point, c: Point) -> bool: Static method to check if three points form a valid triangle.
    """
    a: Point
    b: Point
    c: Point

    def get_area(self) -> float:
        """
        Calculates the area of the triangle using the determinant formula.

        Returns:
        - float: The area of the triangle.
        """
        return 0.5 * abs(
            self.a.x * (self.b.y - self.c.y) +
            self.b.x * (self.c.y - self.a.y) +
            self.c.x * (self.a.y - self.b.y)
        )

    def get_length_side(self) -> Tuple[float, float, float]:
        """
        Computes the lengths of the sides of the triangle.

        Returns:
        - Tuple[float, float, float]: A tuple containing the lengths of the sides (AB, BC, and AC).
        """
        ab = self.a.get_distance_from(self.b)
        bc = self.b.get_distance_from(self.c)
        ac = self.a.get_distance_from(self.c)
        return ab, bc, ac

    def is_right_triangle(self) -> bool:
        """
        Determines if the triangle is a right-angled triangle using the Pythagorean theorem.

        Returns:
        - bool: True if the triangle is right-angled, False otherwise.
        """
        ab2, bc2, ac2 = [x ** 2 for x in self.get_length_side()]
        # print(ab2, bc2, ac2)
        return (
            math.isclose(ab2 + bc2, ac2) or
            math.isclose(ab2 + ac2, bc2) or
            math.isclose(bc2 + ac2, ab2)
        )

    @staticmethod
    def is_triangle(a: Point, b: Point, c: Point) -> bool:
        """

        Checks if three points can form a valid triangle.

        Parameters:
        - a (Point): The first point.
        - b (Point): The second point.
        - c (Point): The third point.

        Returns:
        - bool: True if the points form a valid triangle, False otherwise.
        """
        triangle = Triangle(a, b, c)
        ab, bc, ca = triangle.get_length_side()
        return ab + bc > ca and ab + ca > bc and bc + ca > ab


def get_collinear(p1: Point, p2: Point, p3: Point) -> bool:
    """
    Determines if three points are collinear, meaning they lie on the same straight line.

    Parameters:
    - p1 (Point): The first point.
    - p2 (Point): The second point.
    - p3 (Point): The third point.

    Returns:
    - bool: True if the points are collinear, False otherwise.
    """
    triangle = Triangle(p1, p2, p3)
    return math.isclose(triangle.get_area(), 0.0)
