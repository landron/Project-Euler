# http://projecteuler.net/problem=7
#   What is the 10 001st prime number?
# http://projecteuler.net/problem=10
#   Problem 10. Sum all primes below N million
# Version: 2015.01.04

# TODO: 
#     ? 1. FindPrimesNumberCount, position <= 0
#     2. Other optimizations (sieve)

import math

HARD_VALIDATE = False

def get_primes(limit):

    # initialization 
    primes = [0 for i in range(limit)]
    for i in range(3,limit,2):
        primes[i] = i
    primes[2] = 2

    limit_of_sieve = limit
    # You only need to start crossing out multiples at p^2, because any 
    # smaller multiple of p has a prime divisor less than p and has already 
    # been crossed out as a multipleof that.
    limit_of_sieve = 1 + math.floor(math.sqrt(limit))

    # sieve of Eratosthenes
    for i in range(3,limit_of_sieve,2):
        if primes[i]:
            for j in range(3*i,limit,2*i):
                primes[j] = 0

    return primes

def FindPrimesNumberCount(limit, position = 0):
    primes = get_primes(limit)
    count = 1 #2
    if (1 == position):
        return (1, 2)
    for i in range(3,limit,2):
        if (primes[i]>0):
            count += 1
            if (position == count):
                return (count, i)
    return (count, 0)

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

if __name__ == "__main__":
    validate_FindPrimesNumberCount()
    validate_find_primes_sum()

    print("{:d}".format(FindPrimeNumber(10001)))
    # print("{:d}".format(find_primes_sum(2000000)))