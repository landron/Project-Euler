'''
    http://projecteuler.net/problem=5
        What is the smallest positive number that is evenly divisible by all of the numbers
         from 1 to 20?

    Version: 2016.01.10
        small errors, big consequences

    pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 8.30/10 (previous run: 8.11/10, +0.19)
'''

import math
from itertools import chain

def HighestPower(value, limit):
    assert value < limit
    result = value
    while result < limit:
        result *= value
    return result/value

def ProcessPowers(number, limit, result):
    i = 3*number
    while i < limit:
        result[i] = 0
        i += 2*number

def SieveOfFactors(limit):
    result = [-1 for i in range(1+limit)]

    square_root = 1+int(math.sqrt(limit))

    # process separately since we only keep the highest power
    for i in chain(range(3, square_root, 2)):
        ProcessPowers(i, 1+limit, result)

    # keep only the highest power
    for i in chain([2], range(3, square_root, 2)):
        power = i
        while power <= limit:
            result[int(power)] = 0
            power *= i
        result[int(power/i)] = 1

    for i in range(3, 1+limit, 2):
        if result[i] < 0:
            result[i] = 1
            ProcessPowers(i, limit, result)

    return result

def SmallestMultiple(below):
    sieve = SieveOfFactors(below)
    result = 1
    for i, val in enumerate(sieve):
        if val > 0:
            result *= i
    return result

def debug_validations():
    """all the assertions"""
    assert SmallestMultiple(2) == 2
    assert SmallestMultiple(3) == 6
    assert SmallestMultiple(4) == 12
    assert SmallestMultiple(10) == 2520
    assert SmallestMultiple(11) == 27720
    assert SmallestMultiple(20) == 232792560
    assert SmallestMultiple(21) == SmallestMultiple(20)
    assert SmallestMultiple(21) == SmallestMultiple(22)
    assert SmallestMultiple(23) == 5354228880
    assert SmallestMultiple(26) == 26771144400
    assert SmallestMultiple(28) == SmallestMultiple(27)
    assert SmallestMultiple(28) == 80313433200
    assert SmallestMultiple(31) == 72201776446800

if __name__ == "__main__":
    debug_validations()

    print("{:d}".format(SmallestMultiple(21)))
