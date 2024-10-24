from dataclasses import dataclass
from typing import ClassVar


class VigenereCipher:
    LETTER_A_CODE = 65
    ALPHABET_SIZE = 26

    def __init__(self, key: str) -> None:
        self.key = key

    def encrypt(self, plain_text: str) -> str:
        return self._process_text(plain_text)

    def decrypt(self, ciphet_text: str) -> str:
        return self._process_text(ciphet_text, -1)

    def _process_text(self, text: str, shift_direction: int = 1) -> str:
        processed_text = []
        key_len = len(self.key)
        key_index = 0

        for i, letter in enumerate(text):
            if letter.isupper():
                key_letter = self.key[key_index % key_len]
                shift = (ord(key_letter) - VigenereCipher.LETTER_A_CODE) * shift_direction
                processed_letter = self._shift_letter(letter, shift)
                processed_text.append(processed_letter)
                key_index += 1
            else:
                processed_text.append(letter)

        return ''.join(processed_text)

    def _shift_letter(self, letter: str, shift: int) -> str:
        base = VigenereCipher.LETTER_A_CODE
        shifted = (ord(letter) - base + shift) % VigenereCipher.ALPHABET_SIZE
        return chr(base + shifted)


@dataclass
class CaesarCipher:
    """
    A class representing the Caesar cipher, a substitution cipher where each letter in the plaintext
    is shifted by a fixed number of positions in the alphabet.

    Attributes:
    - key (int): The number of positions to shift each letter by during encryption and decryption.

    Methods:
    - encrypt(text: str) -> str: Encrypts the provided text using the Caesar cipher.
    - decrypt(text: str) -> str: Decrypts the provided text using the Caesar cipher.
    """
    key: int

    CODE_UPPER_A: ClassVar[int] = 65
    CODE_UPPER_Z: ClassVar[int] = 90
    CODE_LOWER_A: ClassVar[int] = 97
    CODE_LOWER_Z: ClassVar[int] = 122
    ALPHABET_LENGTH: ClassVar[int] = 26

    def encrypt_and_decrypt(self, text: str, encrypt: bool) -> str:
        """
        Encrypts or decrypts the given text by shifting each letter according to the Caesar cipher.

        Parameters:
        - text (str): The text to be encrypted or decrypted.
        - encrypt (bool): If True, the function will encrypt the text; if False, it will decrypt the text.

        Returns:
        - str: The encrypted or decrypted text.
        """

        def shift_char(c, shift):
            if c.isupper():
                return chr((ord(c) - CaesarCipher.CODE_UPPER_A + shift) % CaesarCipher.ALPHABET_LENGTH
                           + CaesarCipher.CODE_UPPER_A)
            elif c.islower():
                return chr((ord(c) - CaesarCipher.CODE_LOWER_A + shift) % CaesarCipher.ALPHABET_LENGTH
                           + CaesarCipher.CODE_LOWER_A)
            else:
                return c

        shift = self.key if encrypt else -self.key
        return ''.join(shift_char(c, shift) for c in text)

    def encrypt(self, text: str) -> str:
        """
        Encrypts the given text using the Caesar cipher.

        Parameters:
        - text (str): The plaintext to be encrypted.

        Returns:
        - str: The encrypted ciphertext.
        """
        return self.encrypt_and_decrypt(text, True)

    def decrypt(self, text: str) -> str:
        """
        Decrypts the given ciphertext using the Caesar cipher.

        Parameters:
        - text (str): The ciphertext to be decrypted.

        Returns:
        - str: The decrypted plaintext.
        """
        return self.encrypt_and_decrypt(text, False)
