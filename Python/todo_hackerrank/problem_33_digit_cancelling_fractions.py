#!/bin/python3
'''
    tag_digits

    https://projecteuler.net/problem=33
        Digit cancelling fractions

    https://www.hackerrank.com/contests/projecteuler/challenges/euler033
        !hard
        todo_hackerrank

    pylint 1.5.5
'''

def are_equals(nom1, denom1, nom2, denom2):
    return nom1*denom2 == nom2*denom1

def get_greatest_common_divisor(a, b):
    if a == b:
        return a
    elif a < b:
        return get_greatest_common_divisor(b, a)
    elif b == 0:
        return a
    return get_greatest_common_divisor(b, a%b)

def is_curious(start, end, common, K):
    p_10 = 10**K
    nom = start*p_10+common
    denominator = common*p_10+end
    return are_equals(nom, denominator, start, end)

def is_curious_calc(start, end, common):
    digits = 0
    quot = common
    while quot > 1:
        quot /= 10
        digits += 1
    return is_curious(start, end, common, digits)

def get_not_last_0(N):
    min = 10**N+1
    if min != 1:
        min += 1
    return min

def solve_problem_base(N, K):
    nominator = []
    denominator = []
    
    for i in range(10**(N-K-1), 10**(N-K)):
        # get digits of i, the nominator
        # if > 2, get combinations with the other digits for the denominator
        pass

    return (nominator, denominator)

# https://projecteuler.net/problem=33 only 
def solve_problem_original():
    nominator = []
    denominator = []

    for i in range(10, 100):
        d1 = i//10
        d2 = i%10
        for j in range(1, 10):
            if d1 == d2 == j:
                continue
            if is_curious(d1, d2, j, 1):
                # print("curious: {0}{1}/{1}{2}".format(d1, j, d2))
                nominator.append(d1)
                denominator.append(d2)

    # print(nominator, denominator)
    
    nom = 1
    for i in nominator:
        nom *= i
    denom = 1
    for i in denominator:
        denom *= i

    gcd = get_greatest_common_divisor(nom, denom)
    return denom/gcd

# https://www.hackerrank.com/contests/projecteuler/challenges/euler033 
def solve_problem(N, K):
    pass

# https://www.hackerrank.com/contests/projecteuler/challenges/euler033
def parse_input():
    (N, K) = [int(j) for j in input().strip().split(' ')]
    for _ in range(cases):
        positions = [int(i) for i in input().strip().split(' ')]
        print(solve_problem(positions))

def problem():
    return solve_problem_original()

def debug_assertions():
    assert are_equals(49, 98, 4, 8)
    assert not are_equals(49, 98, 4, 9)

    assert is_curious_calc(1, 4, 6)
    assert is_curious_calc(1, 5, 9)
    assert is_curious_calc(2, 5, 6)
    assert is_curious_calc(4, 8, 9)

    assert get_greatest_common_divisor(42, 28) == 14
    assert get_greatest_common_divisor(42, 56) == 14
    assert get_greatest_common_divisor(54, 24) == 6

def main():
    debug_assertions()

    # parse_input()
    print(problem())

if __name__ == "__main__":
    main()
