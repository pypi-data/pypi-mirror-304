def are_anagram(word1: str, word2: str) -> bool:
    """
    Determines whether two words are anagrams of each other. An anagram is a rearrangement
    of the letters of one word to form another word.

    Parameters:
    - word1 (str): The first word to compare.
    - word2 (str): The second word to compare.

    Returns:
    - bool: True if `word1` and `word2` are anagrams, False otherwise.
    """
    if len(word1) != len(word2):
        return False

    return sorted(word1) == sorted(word2)


def is_palindrome(n: int) -> bool:
    """
    Determines whether the given integer `n` is a palindrome. A palindrome is a number
    that reads the same forward and backward.

    Parameters:
    - n (int): The integer to check for palindrome property.

    Returns:
    - bool: True if `n` is a palindrome, False otherwise.
    """
    if n < 0:
        return False
    n_str = str(n)
    return n_str == n_str[::-1]
