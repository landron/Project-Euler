#!/bin/python3
'''
    https://projecteuler.net/problem=30
        "Find the sum of all the numbers that can be written as the sum of fifth powers of their digits."

    https://www.hackerrank.com/contests/projecteuler/challenges/euler030
        score: 100

    Your code has been rated at 8.14/10 (previous run: 8.14/10, +0.00)
'''

from array import array

def no_digits(n):
    digits = 0
    while n >= 1:
        n //= 10
        digits += 1
    return digits

def get_digits(n):
    digits = []
    while n >= 1:
        digits.append(n%10)
        n //= 10
    return digits

def max_digits_for_power(power):
    term_9 = 9**power

    factor = 2
    digits = no_digits(factor*term_9)
    while digits >= factor:
        digits = no_digits(factor*term_9)
        factor += 1
    return factor-1

def solve_problem(power, to_print=False):

    powers = array('I')
    for i in range(10):
        powers.append(i**power)

    nb_digits = max_digits_for_power(power)
    # digits = array('I')
    # for i in range(nb_digits):
    #     digits.append(0)

    max_nb = nb_digits*powers[9]
    # print(max_nb)
    sum_powers = 0
    # digits[1] = 1
    for i in range(10, max_nb):
        digits = get_digits(i)
        partial = 0
        for j in digits:
            partial += powers[j]
        # print(sum_powers, i)
        if partial == i:
            if to_print:
                print(i)
            sum_powers += i
    return sum_powers

# https://www.hackerrank.com/contests/projecteuler/challenges/euler030
def parse_input():
    power = int(input().strip())
    print(solve_problem(power))

def problem():
    print(solve_problem(5))

def debug_assertions():
    assert no_digits(2) == 1
    assert no_digits(3567) == 4

    assert max_digits_for_power(2) == 3
    assert max_digits_for_power(3) == 4

    assert get_digits(11) == [1, 1]
    assert get_digits(29) == [9, 2]
    assert get_digits(34537) == [7, 3, 5, 4, 3]

    assert solve_problem(2) == 0
    assert solve_problem(3) == 1301
    assert solve_problem(4) == 19316

def main():
    debug_assertions()

    # parse_input()
    problem()

if __name__ == "__main__":
    main()
