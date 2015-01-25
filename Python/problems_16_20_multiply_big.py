"""
    Problem 16 : Power digit sum
    http://projecteuler.net/problem=16
        What is the sum of the digits of the number 2^1000?
    Problem 20 : Factorial digit sum
    http://projecteuler.net/problem=20
        Find the sum of the digits in the number 100!
        
    Version: 2015.01.25

    pylint.bat --version
        No config file found, using default configuration
        pylint 1.4.0,
        astroid 1.3.2, common 0.63.2
        Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  6 2014, 22:15:05) [MSC v.1600 32 bit (Intel)]
    Your code has been rated at 10.00/10
"""

from functools import reduce

def multiply(number, factor):
    """multiply large number by the given factor"""
    number = [factor*i for i in number]
    carry = 0
    result = []
    for i in reversed(number):
        result += [(carry+i)%10]
        carry = (carry+i) // 10
    while carry:
        result += [carry%10]
        carry //= 10
    result.reverse()
    return result

def debug_validations():
    """all the assertions"""
    assert 4662 == reduce(lambda x, y: 10*x+y, multiply([6, 6, 6], 7))
    assert 81918 == reduce(lambda x, y: 10*x+y, multiply([6, 6, 6], 123))

def problem_16():
    """solve the problem"""

    number = [1]
    for i in range(1000):   #pylint: disable=unused-variable
        number = multiply(number, 2)
    result = sum(number)
    assert 1366 == result
    print("Result 16: {0}".format(result))

def problem_20():
    """solve the problem"""

    number = [1]
    for i in range(100):
        number = multiply(number, i+1)
    result = sum(number)
    assert 648 == result
    print("Result 20: {0}".format(result))

if __name__ == "__main__":
    debug_validations()

    problem_16()
    problem_20()
