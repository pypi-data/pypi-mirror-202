from random import randint


def D6() -> str:
    """
    Roll a D6
    :return: an integer between 1 and 6 included
    """
    return str(randint(1, 6))


def D66() -> str:
    """
    Roll a D66
    :return: a string that is the concatenation of two D6 rolls
    """
    return D6() + D6()
