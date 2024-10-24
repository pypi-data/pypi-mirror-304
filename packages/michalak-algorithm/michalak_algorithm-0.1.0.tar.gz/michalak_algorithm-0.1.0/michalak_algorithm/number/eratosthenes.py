from typing import Self


class EratostenesSieve:
    """
    Implements the Sieve of Eratosthenes algorithm for finding prime numbers.

    Attributes:
    - sieve (list[int]): A list representing whether numbers are prime (1) or not (0).

    Methods:
    - is_prime(v: int) -> bool: Checks if a number is prime using the precomputed sieve.
    - of(n: int) -> Self: Class method that generates a sieve up to a given number `n`.
    """
    sieve: list[int]

    def __init__(self, sieve: list[int]) -> None:
        """
        Initializes the sieve with a given list of primes.

        Parameters:
        - sieve (list[int]): A list where prime numbers are marked as 1 and non-prime as 0.
        """
        self.sieve = sieve

    def is_prime(self, v: int) -> bool:
        """
        Checks if a given number `v` is prime by consulting the sieve.

        Parameters:
        - v (int): The number to check for primality.

        Returns:
        - bool: True if `v` is prime, False otherwise.
        """
        return 0 <= v < len(self.sieve) and self.sieve[v] == 1

    @classmethod
    def of(cls, n: int) -> Self:
        """
        Class method that generates a Sieve of Eratosthenes for numbers up to `n`.

        Parameters:
        - n (int): The upper limit for prime number generation.

        Returns:
        - EratostenesSieve: An instance of `EratostenesSieve` with the sieve filled.
        """
        sieve = [0, 0] + [1] * (n - 1)
        p = 2
        while p * p <= n:
            if sieve[p] == 1:
                for i in range(p * p, n + 1, p):
                    sieve[i] = 0
            p += 1
        return cls(sieve)
