'''
    http://projecteuler.net/problem=7
      What is the 10 001st prime number?
    http://projecteuler.net/problem=10
      Problem 10. Sum all primes below N million

    Version: 2016.01.10

    TODO: 
        ? 1. FindPrimesNumberCount, position <= 0
        2. FindPrimesNumberCount is still not fast enough (Sieve of Eratosthenes) for the latest test case of
        http://www.hackerrank.com/contests/projecteuler/challenges/euler007
        See http://math.stackexchange.com/questions/1257/is-there-a-known-mathematical-equation-to-find-the-nth-prime
'''

HARD_VALIDATE = False

from math import log
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
    # Consequence Two: The nth prime is about n (ln n + ln (ln n))
    if position >= 6:
        limit = 1 + int(position * (log(position)+log(log(position))))
    # print(position, limit)

    # prime = 0
    # while (0 == prime):
    #     (count, prime) = FindPrimesNumberCount(limit, position) 
    #     limit *= 10
    # return prime
    result = FindPrimesNumberCount(limit, position)[1]
    assert result != 0
    return result

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
    assert(5 == FindPrimeNumber(3))
    assert(13 == FindPrimeNumber(6))

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
def problem_10():
    """solve the problem, print the needed time"""
    start = time()
    result = find_primes_sum(2000000)
    assert 142913828922 == result
    print("Problem 11 - result {0:d} in {1:.2f} seconds".format(result, time()-start))

if __name__ == "__main__":
    validate_FindPrimesNumberCount()
    validate_find_primes_sum()

    problem_7()
    # problem_10()

    # for i in range(1,100):
    #     print(FindPrimeNumber(i))
