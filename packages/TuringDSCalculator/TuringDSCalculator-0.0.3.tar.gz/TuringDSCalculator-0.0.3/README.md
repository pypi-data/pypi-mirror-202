# Turing Data Science Calculator

`TuringDSCalculator` contains simple Calculator that can perform the following operations:

-   _add_ - add the current value with a number.
-   _subtract_ - subtract a number from the current value.
-   _multiply_ - multiply the current value by a number.
-   _divided_ - divide the current value by a number.
-   _root_ - take the n-th root of the current value.
-   _reset_ - change the current value back to default, 0.

Its memory is limited at 1.7976931348623157e+308

## Installation

```sh
pip install TuringDSCalculator
```

## Usage

Using the 5 operations in Calculator:

```python
>>> from TuringDSCalculator import Calculator

# Create a new instance of Calculator
calculator = Calculator()

# Add two numbers
calculator.add(3)
calculator.add(7)

# Get the result
result = calculator.getResult()
print(result) # Output: 10.0

# Subtract a number
calculator.subtract(2)

# Get the result
result = calculator.getResult()
print(result) # Output: 8.0

# Multiply by a number
calculator.multiply(5)

# Get the result
result = calculator.getResult()
print(result) # Output: 40.0

# Divide by a number
calculator.divided(2)

# Get the result
result = calculator.getResult()
print(result) # Output: 20.0

# Take the 3rd root of the current value
calculator.root(3)

# Get the result
result = calculator.getResult()
print(result) # Output: 2.7144176165949083

# Reset the calculator's memory to 0
calculator.reset()

# Get the result
result = calculator.getResult()
print(result) # Output: 0.0

```

## Contributing
I welcome pull requests for this Sprint 1 project. If you plan to make significant changes, I recommend that you open an issue first to discuss your proposed changes. Please ensure that you add or update tests as appropriate.

## [Changelog](CHANGELOG.md)

## License

[MIT](https://choosealicense.com/licenses/mit/)
