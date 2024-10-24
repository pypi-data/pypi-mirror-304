import math
from typing import Callable


def is_prime(n: int, i: int) -> bool:
    """
    Determines whether the given integer `n` is a prime number. This function uses
    an iterative approach starting at `i` to check for divisibility.

    Parameters:
    - n (int): The integer to check for primality.
    - i (int): The starting divisor for checking primality (usually set to 5).

    Returns:
    - bool: True if `n` is a prime number, False otherwise.
    """
    if n < 2:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def prime_factors(n: int) -> list[int]:
    """
    Returns the prime factors of the given integer `n`. The function iteratively
    divides `n` by prime numbers starting from 2 and returns a list of factors.

    Parameters:
    - n (int): The integer to factorize.

    Returns:
    - list[int]: A list containing the prime factors of `n`.
    """
    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1

    if n > 1:
        factors.append(n)
    return factors


def sum_digits(n: int) -> int:
    """
    Calculates the sum of the digits of an integer `n`.

    Parameters:
    - n (int): The integer whose digits will be summed.

    Returns:
    - int: The sum of the digits of `n`.
    """
    nn = abs(n)
    s = 0
    while nn > 0:
        s += nn % 10
        nn //= 10
    return s


def get_digit_at(n: int, pos: int) -> int:
    """
    Retrieves the digit at a specified position in an integer `n`. Positions
    are zero-indexed, starting from the right.

    Parameters:
    - n (int): The integer to extract the digit from.
    - pos (int): The position of the digit (zero-indexed from the right).

    Returns:
    - int: The digit at the specified position.

    Raises:
    - ValueError: If the position is out of range.
    """
    if pos < 0:
        raise ValueError('Position out of range')
    return (abs(n) // 10 ** pos) % 10


def divisors_number(n: int) -> int | float:
    """
    Calculates the number of divisors of an integer `n`. If `n` is zero,
    returns infinity as zero has infinite divisors.

    Parameters:
    - n (int): The integer for which to count divisors.

    Returns:
    - int | float: The number of divisors of `n`, or infinity if `n` is zero.
    """
    if n == 0:
        return math.inf

    if n == 1:
        return 1

    cnt = 2

    i = 2
    while i * i < n:
        if n % i == 0:
            cnt += 2
        i += 1

    if i * i == n:
        cnt += 1

    return cnt


def factorial_recursive(n: int) -> int:
    """
    Recursively calculates the factorial of the given integer `n`.

    Parameters:
    - n (int): The integer to compute the factorial of.

    Returns:
    - int: The factorial of `n`.
    """
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
    """
    Iteratively calculates the factorial of the given integer `n`.

    Parameters:
    - n (int): The integer to compute the factorial of.

    Returns:
    - int: The factorial of `n`.
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def factorial_function(n: int) -> int:
    """
    Calculates the factorial of the given integer `n` using Python's built-in
    `math.factorial()` function.

    Parameters:
    - n (int): The integer to compute the factorial of.

    Returns:
    - int: The factorial of `n`.
    """
    return math.factorial(n)


def fast_exponentiation(a: int, n: int) -> int:
    """
    Performs fast exponentiation, calculating `a` raised to the power of `n`
    using an efficient iterative approach (exponentiation by squaring).

    Parameters:
    - a (int): The base number.
    - n (int): The exponent.

    Returns:
    - int: The result of `a` raised to the power of `n`.
    """
    result = 1

    while n > 0:
        if n % 2 == 1:
            result *= a
        a *= a
        n //= 2

    return result


def sqrt(x: int) -> tuple[float, float]:
    """
    Computes the square root of a given integer `x` using Newton's method.
    The function returns both the square root and the square of that value
    for accuracy.

    Parameters:
    - x (int): The integer to compute the square root of.

    Returns:
    - tuple[float, float]: A tuple containing the square root and the square of that value.
    """
    if x == 0:
        return 0, 0

    tolerance = 1e-10
    y = x
    i = 0

    while True:
        next_y = (y + x / y) / 2
        i += 1

        if abs(y - next_y) < tolerance:
            break

        y = next_y

    sqrt_value = float(y)
    squared_value = sqrt_value * sqrt_value

    return sqrt_value, squared_value


def horner(wsp: list[int], st: int, x: int) -> float:
    """
    Evaluates a polynomial using Horner's method for a given value of `x`.

    Parameters:
    - wsp (list[int]): The coefficients of the polynomial.
    - st (int): The degree of the polynomial.
    - x (int): The value at which to evaluate the polynomial.

    Returns:
    - float: The result of the polynomial evaluated at `x`.
    """
    result = wsp[0]
    for i in range(1, st + 1):
        result = result * x + wsp[i]
    return result


def coprime_numbers(a: int, b: int, p: int) -> list[int]:
    """
    Finds all numbers in the range `[a, b]` that are coprime with `p`. Two numbers
    are coprime if their greatest common divisor (gcd) is 1.

    Parameters:
    - a (int): The lower bound of the range.
    - b (int): The upper bound of the range.
    - p (int): The number to check for coprimality.

    Returns:
    - list[int]: A list of numbers between `a` and `b` that are coprime with `p`.
    """
    result = []
    for i in range(a, b + 1):
        if math.gcd(i, p) == 1:
            result.append(i)
    return result


def bisection(a: float, b: float, epsilon: float, fn: Callable[[float], float]) -> float:
    """
    Finds the root of a continuous function `fn` within the interval `[a, b]`
    using the bisection method, stopping when the interval is smaller than `epsilon`.

    Parameters:
    - a (float): The lower bound of the interval.
    - b (float): The upper bound of the interval.
    - epsilon (float): The desired precision of the result.
    - fn (Callable[[float], float]): The continuous function whose root is to be found.

    Returns:
    - float: The approximate root of the function within the interval.

    Raises:
    - ValueError: If the function does not change signs over the interval.
    """
    if fn(a) * fn(b) > 0:
        raise ValueError('Roots not found')
    if fn(a) == 0:
        return a
    if fn(b) == 0:
        return b
    while (b - a) / 2 > epsilon:
        mid = (a + b) / 2
        if fn(mid) == 0:
            return mid
        elif fn(a) * fn(mid) < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2


def integrate_trapeze_method(l: float, u: float, n: int, fn: Callable[[float], float]) -> float:
    """
    Approximates the integral of a function `fn` over the interval `[l, u]` using the trapezoidal method with `n`
    subintervals.

    Parameters:
    - l (float): The lower bound of the integral.
    - u (float): The upper bound of the integral.
    - n (int): The number of subintervals.
    - fn (Callable[[float], float]): The function to integrate.

    Returns:
    - float: The approximate value of the integral.
    """
    dx = (u - l) / n
    integral = 0.5 * (fn(l) + fn(u))
    for i in range(1, n):
        x = l + i * dx
        integral += fn(x)
    integral *= dx

    return integral


def integrate_rectangle_method(l: float, u: float, n: int, fn: Callable[[float], float]) -> float:
    """
    Approximates the integral of a function `fn` over the interval `[l, u]` using the rectangle method (midpoint rule) with `n` subintervals.

    Parameters:
    - l (float): The lower bound of the integral.
    - u (float): The upper bound of the integral.
    - n (int): The number of subintervals.
    - fn (Callable[[float], float]): The function to integrate.

    Returns:
    - float: The approximate value of the integral.
    """
    dx = (u - l) / n
    x = l
    full_area = 0
    for i in range(n):
        x += (i + 1) * dx / 2
        full_area += fn(x) * dx
    return full_area
