# TURING CALCULATOR
# ----------------------------------------------------------------------------------------------------------------
"""
    A simple calculator that can perform the following operations:

    - Addition: add two numbers and return the result.
    - Subtraction: subtract two numbers and return the result.
    - Multiplication: multiply two numbers and return the result.
    - Division: divide two numbers and return the result.
    - Find root: take the n-th root of a number and return the result.
    - Reset memory: reset the calculator's memory to 0.

    Its memory is limited at 1.7976931348623157e+308
"""

__version__ = "0.0.3"


# START --------
import doctest
from numbers import Number


# EXECUTION ----
LIMIT = 1.7976931348623157e+308


class Calculator(object):
    """
    A simple calculator that can perform the following operations:

    - Addition: add two numbers and return the result.
    - Subtraction: subtract two numbers and return the result.
    - Multiplication: multiply two numbers and return the result.
    - Division: divide two numbers and return the result.
    - Find root: take the n-th root of a number and return the result.
    - Reset memory: reset the calculator's memory to 0.

    Usage: an instance of Calculator takes 1 optional argument as the default value.

    - To perform an operation, call the relevant method on the instance.
    - To access the result of the previous operation, use the 'getResult' method.
    - To reset the calculator's memory to 0, use the `resetMemory` method.

    Example usage:

    >>> calculator = Calculator()
    >>> calculator.add(9)
    >>> calculator.getResult()
    9
    >>> calculator.subtract(5)
    >>> calculator.getResult()
    4
    >>> calculator.multiply(6)
    >>> calculator.getResult()
    24
    >>> calculator.divided(3)
    >>> calculator.getResult()
    8.0
    >>> calculator.root(3)
    >>> calculator.getResult()
    2.0
    >>> calculator.reset()
    >>> calculator.getResult()
    0
    """

    def __init__(self, default: float=0) -> None:
        self.__value = default
        
    def add(self, term: float) -> None:
        """
        Usage: increase current value by <term>
        """
        if not isinstance(term, Number):
            raise TypeError('Invalid value to add with.')
        self.__value += float(term)

    def subtract(self, term: float) -> None:
        """
        Increase current value by <term>
        """
        if not isinstance(term, Number):
            raise TypeError('Invalid value to subtract from.')
        self.__value -= float(term)

    def multiply(self, factor: float) -> None:
        """
        Usage: find the  current value by <term>
        """
        if not isinstance(factor, Number):
            raise TypeError('Invalid value to multiply with.')
        self.__value *= float(factor)

    def divided(self, divisor: float) -> None:
        """
        Usage: divide current value by <divisor>
        """
        if not isinstance(divisor, Number):
            raise TypeError('Invalid value to divide by.')
        elif divisor == 0:
            raise ZeroDivisionError('Divisor cannot be 0.')
        self.__value /= float(divisor)

    def root(self, degree: float) -> None:
        """
        Usage: find the <degree>-th root of current value
        """
        if not isinstance(degree, Number):
            raise TypeError('Invalid value as root.')
        try:
            self.__value **= 1/float(degree)
        except OverflowError:
            self.__value = LIMIT

    def reset(self) -> None:
        """
        Usage: reset the calculator
        """
        self.__value = 0

    def getResult(self) -> float:
        """
        Usage: get current value in memory
        """
        return self.__value


# END ----------
if __name__ == '__main__':
    print(doctest.testmod())
