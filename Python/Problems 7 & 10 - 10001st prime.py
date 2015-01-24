# http://projecteuler.net/problem=7
#   What is the 10 001st prime number?
# http://projecteuler.net/problem=10
#   Problem 10. Sum all primes below N million
# Version: 2015.01.04

# TODO: 
#     ? 1. FindPrimesNumberCount, position <= 0

HARD_VALIDATE = False

from time import time
from proj_euler import get_primes

def FindPrimesNumberCount(limit, position = 1):
    assert position > 0
    primes = get_primes(limit)
    if position-1 < len(primes):
        return (len(primes), primes[position-1])
    return (len(primes), 0)

def FindPrimeNumber(position):
    limit = 100
    prime = 0
    while (0 == prime):
        limit *= 10
        (count, prime) = FindPrimesNumberCount(limit, position) 
    return prime

def find_primes_sum(limit):
    primes = get_primes(limit)
    # print(primes)
    return sum(primes)

def validate_FindPrimesNumberCount():
    assert(25 == FindPrimesNumberCount(100)[0])
    assert(168 == FindPrimesNumberCount(1000)[0])
    assert(1229 == FindPrimesNumberCount(10000)[0])
    if HARD_VALIDATE:
        assert(9592 == FindPrimesNumberCount(100000)[0])
        assert(78498 == FindPrimesNumberCount(1000000)[0])
    assert(13 == FindPrimeNumber(6))
    assert(97 == FindPrimeNumber(25))
    assert(997 == FindPrimeNumber(168))

def validate_find_primes_sum():
    assert (17 == find_primes_sum(9))
    assert (17 == find_primes_sum(10))
    assert (17 == find_primes_sum(11))
    assert (28 == find_primes_sum(12))
    assert (100 == find_primes_sum(29))
    assert (129 == find_primes_sum(30))
    assert (1060 == find_primes_sum(100))
    assert (76127 == find_primes_sum(1000))
    assert (5736396 == find_primes_sum(10000))
    assert (32405717 == find_primes_sum(25000))
    if HARD_VALIDATE:
        assert (142913828922 == find_primes_sum(2000000))

# 0.5 - 0.6 seconds
def problem_7():
    """solve the problem, print the needed time"""
    start = time()
    result = FindPrimeNumber(10001)
    assert 104743 == result
    print("Problem 7 - result {0:d} in {1:.2f} seconds".format(result, time()-start))

# around 1 second, be aware of the validations
def problem_11():
    """solve the problem, print the needed time"""
    start = time()
    result = find_primes_sum(2000000)
    assert 142913828922 == result
    print("Problem 11 - result {0:d} in {1:.2f} seconds".format(result, time()-start))

if __name__ == "__main__":
    validate_FindPrimesNumberCount()
    validate_find_primes_sum()

    problem_7()
    # problem_11()
