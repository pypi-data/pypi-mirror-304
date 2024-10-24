from abc import ABC, abstractmethod
from math import gcd


class Gcd(ABC):
    """
    Abstract base class for computing the greatest common divisor (GCD) of two integers.

    Methods:
    - get_value(a: int, b: int) -> int: Abstract method to compute the GCD of two integers `a` and `b`.
    """

    @abstractmethod
    def get_value(self, a: int, b: int) -> int:
        """
        Computes the GCD of two integers `a` and `b`. This method must be implemented by subclasses.

        Parameters:
        - a (int): The first integer.
        - b (int): The second integer.

        Returns:
        - int: The greatest common divisor of `a` and `b`.
        """
        pass


class GcdSubIter(Gcd):
    """
    Class that computes the GCD using the iterative subtraction method.

    Methods:
    - get_value(a: int, b: int) -> int: Iteratively computes the GCD by repeated subtraction.
    """

    def get_value(self, a: int, b: int) -> int:
        """
        Iteratively computes the GCD of two integers `a` and `b` using the subtraction method.

        Parameters:
        - a (int): The first integer.
        - b (int): The second integer.

        Returns:
        - int: The greatest common divisor of `a` and `b`.
        """
        while a != b:
            if a > b:
                a -= b
            else:
                b -= a
        return a


class GcdSubRec(Gcd):
    """
    Class that computes the GCD using the recursive subtraction method.

    Methods:
    - get_value(a: int, b: int) -> int: Recursively computes the GCD by repeated subtraction.
    """

    def get_value(self, a: int, b: int) -> int:
        """
        Recursively computes the GCD of two integers `a` and `b` using the subtraction method.

        Parameters:
        - a (int): The first integer.
        - b (int): The second integer.

        Returns:
        - int: The greatest common divisor of `a` and `b`.
        """
        if a == b:
            return a
        elif a > b:
            return self.get_value(a - b, b)
        else:
            return self.get_value(a, b - a)


class GcdModIter(Gcd):
    """
    Class that computes the GCD using the iterative modulus (Euclidean) method.

    Methods:
    - get_value(a: int, b: int) -> int: Iteratively computes the GCD using the modulus operation.
    """

    def get_value(self, a: int, b: int) -> int:
        """
        Iteratively computes the GCD of two integers `a` and `b` using the modulus (Euclidean) method.

        Parameters:
        - a (int): The first integer.
        - b (int): The second integer.

        Returns:
        - int: The greatest common divisor of `a` and `b`.
        """
        while b:
            a, b = b, a % b
        return a


class GcdModRec(Gcd):
    """
    Class that computes the GCD using the recursive modulus (Euclidean) method.

    Methods:
    - get_value(a: int, b: int) -> int: Recursively computes the GCD using the modulus operation.
    """

    def get_value(self, a: int, b: int) -> int:
        """
        Recursively computes the GCD of two integers `a` and `b` using the modulus (Euclidean) method.

        Parameters:
        - a (int): The first integer.
        - b (int): The second integer.

        Returns:
        - int: The greatest common divisor of `a` and `b`.
        """
        if b == 0:
            return a
        return self.get_value(b, a % b)


class GcdBultIn(Gcd):
    """
    Class that computes the GCD using Python's built-in math.gcd function.

    Methods:
    - get_value(a: int, b: int) -> int: Computes the GCD using the built-in `gcd` function from the `math` module.
    """

    def get_value(self, a: int, b: int) -> int:
        """
        Computes the GCD of two integers `a` and `b` using the built-in `gcd` function from the `math` module.

        Parameters:
        - a (int): The first integer.
        - b (int): The second integer.

        Returns:
        - int: The greatest common divisor of `a` and `b`.
        """
        return gcd(a, b)
