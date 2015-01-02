# http://projecteuler.net/problem=5
# Version: 2014.01.16

import math
from itertools import chain

def HighestPower(value, limit):
    assert (value < limit)
    result = value
    while (result < limit):
        result *= value
    return result/value

def ProcessPowers(number, limit, result):
    i = 3*number
    while (i < limit):
        result[i] = 0
        i += 2*number

def SieveOfFactors(limit):
    result = [-1 for i in range(limit)]

    squareRoot = 1+int(math.sqrt(limit))

    # process separately since we only keep the highest power
    for i in chain(range(3, squareRoot, 2)):
        ProcessPowers(i, limit, result)

    # keep only the highest power
    for i in chain([2], range(3, squareRoot, 2)):
        power = i
        while (power < limit):
            result[int(power)] = 0
            power *= i
        result[int(power/i)] = 1

    for i in range(3, limit, 2):
        if (result[i] < 0):
            result[i] = 1
            ProcessPowers(i, limit, result)

    return result

def SmallestMultiple(below):
    sieve = SieveOfFactors(below)
    result = 1
    for i, val in enumerate(sieve):
        if (val > 0):
            result *= i
    return result

if __name__ == "__main__":
    assert (2520 == SmallestMultiple(11))
    assert (232792560 == SmallestMultiple(21))
    assert (SmallestMultiple(23) == SmallestMultiple(21))
    assert (SmallestMultiple(20) == SmallestMultiple(21))
    assert (26771144400 == SmallestMultiple(26))
    assert (SmallestMultiple(26) == SmallestMultiple(27))
    assert (80313433200 == SmallestMultiple(28))
    assert (2329089562800 == SmallestMultiple(31))

    print("{:d}".format(SmallestMultiple(21)))