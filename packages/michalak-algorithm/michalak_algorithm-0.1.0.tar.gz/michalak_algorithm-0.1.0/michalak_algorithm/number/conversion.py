from dataclasses import dataclass


@dataclass
class Conversion:
    """
    Implements methods for converting numbers between decimal and other bases (between 2 and 36).

    Attributes:
    - base (int): The base for conversion.

    Methods:
    - decimal_to_base(number: int) -> str: Converts a decimal number to a specified base.
    - base_to_decimal(s: str) -> int: Converts a number from a specified base to decimal.
    - convert_base(s: str, from_base: int, to_base: int) -> str: Converts a number from one base to another.
    """
    base: int

    def decimal_to_base(self, number: int) -> str:
        """
        Converts a decimal number to a string in the specified base.

        Parameters:
        - number (int): The decimal number to convert.

        Returns:
        - str: The converted number in the specified base.

        Raises:
        - ValueError: If the number is negative or if the base is not between 2 and 36.
        """
        if number < 0:
            raise ValueError("Number is negative")

        if not (2 <= self.base <= 36):
            raise ValueError('Base must be between 2 and 36.')

        zero_code = ord('0')
        a_code = ord('A')

        res = ''
        while number > 0:
            reminder = number % self.base
            if reminder < 10:
                res = chr(zero_code + reminder) + res
            else:
                res = chr(a_code + reminder - 10) + res
            number //= self.base

        return res or '0'

    def base_to_decimal(self, s: str) -> int:
        """
        Converts a number from the specified base to decimal.

        Parameters:
        - s (str): The number in the base to convert from.

        Returns:
        - int: The decimal representation of the number.

        Raises:
        - ValueError: If the base is not between 2 and 36 or if the input contains invalid characters.
        """
        if not (2 <= self.base <= 36):
            raise ValueError('Base must be between 2 and 36.')

        lower_s = s.lower()
        zero_code = ord('0')
        a_code = ord('a')

        res = 0
        for c in lower_s:
            if '0' <= c <= '9':
                v = ord(c) - zero_code
            else:
                v = ord(c) - a_code + 10
            if not (0 <= v < self.base):
                raise ValueError('Value is not correct')

            res = res * self.base + v

        return res

    @staticmethod
    def convert_base(s: str, from_base: int, to_base: int) -> str:
        """
        Converts a number from one base to another.

        Parameters:
        - s (str): The number to convert as a string.
        - from_base (int): The base the number is currently in.
        - to_base (int): The base to convert the number to.

        Returns:
        - str: The number converted to the new base.

        Raises:
        - ValueError: If the bases are not between 2 and 36.
        """
        decimal_v = Conversion(from_base).base_to_decimal(s)
        return Conversion(to_base).decimal_to_base(decimal_v)
