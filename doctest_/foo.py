def square(x):
    """Squares x.

    >>> square(2)
    4
    >>> square(-2)
    4
    """

    return x * x

if __name__ == '__main__':
    import sys
    import doctest
    if doctest.testmod().failed:
        raise SystemExit(1)
