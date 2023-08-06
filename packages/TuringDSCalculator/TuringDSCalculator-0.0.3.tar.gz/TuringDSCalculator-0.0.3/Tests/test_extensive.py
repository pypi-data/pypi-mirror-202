# EXTENSIVE TEST FOR CALCULATOR
# ----------------------------------------------------------------------------------------------------------------


# START --------
from TuringDSCalculator import Calculator, LIMIT
from hypothesis import given, assume, strategies, settings, HealthCheck
from math import isnan, isinf, fsum, isclose


# EXECUTION ----
@given(
    strategies.floats(),
    strategies.floats()
)
def test_add_ext(default, term):
    # Remove non-numeric cases
    assume(not isnan(default) and not isnan(term))
    assume(not isinf(default) and not isinf(term))
    assume(abs(default) < LIMIT - abs(term))

    calculator = Calculator(default)
    calculator.add(term)

    assert calculator.getResult() == fsum((default, term))


@given(
    strategies.floats(),
    strategies.floats()
)
def test_subtract_ext(default, term):
    # Remove non-numeric cases
    assume(not isnan(default) and not isnan(term))
    assume(not isinf(default) and not isinf(term))
    assume(abs(default) + abs(term) < LIMIT)

    calculator = Calculator(default)
    calculator.subtract(term)

    assert calculator.getResult() == fsum((default, -term))


@given(
    strategies.floats(),
    strategies.floats()
)
def test_multiply_ext(default, factor):
    # Remove non-numeric cases
    assume(not isnan(default) and not isnan(factor))
    assume(not isinf(default) and not isinf(factor))

    calculator = Calculator(default)
    calculator.multiply(factor)

    assert calculator.getResult() == default*factor


@given(
    strategies.floats(),
    strategies.floats()
)
def test_divide_ext(factor, divisor):
    # Remove non-numeric cases
    assume(not isnan(factor) and not isnan(divisor))
    assume(not isinf(factor) and not isinf(divisor))

    # Make sure divisor is greater than 0
    assume(abs(divisor) > 1e-100)

    default = factor*divisor
    assume(not isinf(default))

    calculator = Calculator(default)
    calculator.divided(divisor)

    assert isclose(calculator.getResult(), factor, abs_tol=1e-100)


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    strategies.floats(),
    strategies.floats()
)
def test_root_ext(exponent, degree):
    # Remove non-numeric cases
    assume(not isnan(exponent) and not isnan(degree))
    assume(not isinf(exponent) and not isinf(degree))

    # degree is greater than 0
    assume(degree > 1e-5)

    # Make sure exponent value is in possible range and not over limit
    assume((LIMIT**(1/degree) > abs(exponent)) if degree > 1 else True)
    assume(LIMIT > exponent > 1e-10)

    default = exponent**degree
    inverse = 1/degree

    # Make sure default value is in possible range and not over limit
    assume(default > 1e-10 and not isinf(default) and abs(default) < LIMIT)
    assume(inverse != 0.0 and not isinf(inverse) and abs(inverse) < LIMIT)

    calculator = Calculator(default)
    calculator.root(degree)

    assert isclose(calculator.getResult(), exponent, abs_tol=1e-5)


# # END ----------
# if __name__ == '__main__':
#     answer = main()
#     if answer is not None:
#         print(answer)
