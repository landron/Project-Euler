# http://projecteuler.net/problem=7
#   What is the 10 001st prime number?
# Version: 2014.01.16

# TODO: 1. FindPrimesNumberCount, position <= 0

def FindPrimesNumber(limit):
    primes = [-1 for i in range(limit)]
    for i in range(3,limit,2):
        if primes[i] < 0:
            primes[i] = 1
            for j in range(3*i,limit,2*i):
                primes[j] = 0
    return primes

def FindPrimesNumberCount(limit, position = 0):
    primes = FindPrimesNumber(limit)
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

if __name__ == "__main__":
    assert(25 == FindPrimesNumberCount(100)[0])
    assert(168 == FindPrimesNumberCount(1000)[0])
    assert(1229 == FindPrimesNumberCount(10000)[0])
    if 0:
        assert(9592 == FindPrimesNumberCount(100000)[0])
        assert(78498 == FindPrimesNumberCount(1000000)[0])
    assert(13 == FindPrimeNumber(6))
    assert(97 == FindPrimeNumber(25))
    assert(997 == FindPrimeNumber(168))

    print("{:d}".format(FindPrimeNumber(10001)))