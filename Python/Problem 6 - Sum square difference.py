'''
    http://projecteuler.net/problem=6
      Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.
    Version: 2014.01.16

    http://www.hackerrank.com/contests/projecteuler/challenges/euler006
        Difficulty: Easy, passed
'''

import math

def SumSquareDifference(limit):
    sumOf = int(limit*(1+limit)/2)
    result = 0
    for i in range(1, 1+limit):
        result += i*(sumOf-i)
    return result

# g = sum of squares
# g(n) = an3 + bn2 + cn + d,
# g(0) = 0; g(1) = 1; g(2) = 5; g(3) = 14.
# g(n) = n/6 (2n+1)(n+1)
# f(0) = 0; f(n) = f(n-1)+(n-1)*n*n;

def SumSquareDifference2(limit):
    sumOf = int(limit*(1+limit)/2)
    sumOfSquares = int(limit*(1+limit)*(1+2*limit)/6)
    return (sumOf*sumOf-sumOfSquares)

if __name__ == "__main__":
    assert(SumSquareDifference(1) == SumSquareDifference(0))
    assert(SumSquareDifference(1) == SumSquareDifference2(1))
    assert(4 == SumSquareDifference(2))
    assert(SumSquareDifference(2) == SumSquareDifference2(2))
    assert(22 == SumSquareDifference(3))
    assert(SumSquareDifference(3) == SumSquareDifference2(3))
    assert(70 == SumSquareDifference(4))
    assert(SumSquareDifference(4) == SumSquareDifference2(4))
    assert(2640 == SumSquareDifference(10))
    assert(SumSquareDifference(10) == SumSquareDifference2(10))
    assert(25164150 == SumSquareDifference(100))
    assert(SumSquareDifference(100) == SumSquareDifference2(100))

    print("{:d}".format(SumSquareDifference(100)))