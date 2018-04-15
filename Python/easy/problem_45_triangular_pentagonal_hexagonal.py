#!/bin/python3
'''
    https://projecteuler.net/problem=45
        Triangular, pentagonal, and hexagonal

    https://www.hackerrank.com/contests/projecteuler/challenges/euler045
        Score: 100.00

    pylint 1.8.1
        Your code has been rated at 6.36/10.
'''

def solve_problem_original():
    '''
        Find the second number that satisfies the three properties.

        T285 = P165 = H143 = 40755
    '''

    h = 143
    p = 165
    # any hexagonal number is also triangular: n in T is 2n-1 in P
    # t = 285

    # now find the next one
    h += 1

    next_p = p*(3*p-1)//2
    next_h = h*(2*h-1)
    while next_h != next_p:
        while next_h < next_p:
            h += 1
            next_h = h*(2*h-1)
        while next_h > next_p:
            p += 1
            next_p = p*(3*p-1)//2

    return next_p

def solve_problem(limit, use_triangular):
    '''
        hackerrank conditions: all the numbers to a given limit satisfying a relaxed condition
    '''
    result = []

    h = p = t = 1
    next_p = next_h = next_t = 1
    while next_p < limit and next_h < limit:
        if not use_triangular:
            while next_h < next_p:
                h += 1
                next_h = h*(2*h-1)
            while next_h > next_p:
                p += 1
                next_p = p*(3*p-1)//2

            if next_p == next_h:
                result += [next_p]

                p += 1
                next_p = p*(3*p-1)//2

        else:
            while next_t < next_p:
                t += 1
                next_t = t*(t+1)//2
            while next_t > next_p:
                p += 1
                next_p = p*(3*p-1)//2

            if next_p == next_t:
                result += [next_p]

                p += 1
                next_p = p*(3*p-1)//2

    return result

def parse_input():
    '''
        https://www.hackerrank.com/contests/projecteuler/challenges/euler033
    '''
    (N, a, b) = (int(i) for i in input().strip().split(' '))
    result = solve_problem(N, a == 3 or b == 3)
    for i in result:
        print(i)

def problem():
    return solve_problem_original()

def debug_assertions():
    pass

def main():
    debug_assertions()

    # parse_input()
    # print(solve_problem(100000, False))
    print(problem())

if __name__ == "__main__":
    main()
