#! /usr/bin/python3
"""
https://projecteuler.net/problem=40

https://www.hackerrank.com/contests/projecteuler/challenges/euler040
    Score: 100

"Your code has been rated at 10.00/10"
pylint --version
    No config file found, using default configuration
    pylint 1.8.1,
    astroid 1.6.0
    Python 3.6.4
"""


def get_digit_position(nth):
    """
    get the nth digit in Champernowne's constant
    returns the number of digits and the digit position in the sequence
    """
    total_digits = 0
    i = 1
    while True:
        digits = 9 * 10 ** (i - 1) * i
        if nth < total_digits + digits:
            break
        total_digits += digits
        i += 1
    return (i, nth - total_digits)


def solve_problem(indexes):
    """
    tries:  4480 (by error), 1120
    """
    assert len(indexes) == 7

    prod = 1

    for i in range(7):
        current = indexes[7 - i - 1]
        # print(current)
        (digits, pos) = get_digit_position(current)
        # print(digits, pos)
        number = 10 ** (digits - 1) + pos // digits
        digit_in_number = digits - pos % digits if pos % digits != 0 else 0
        if digit_in_number == 0:
            number -= 1
        current_digit = (number // 10**digit_in_number) % 10
        # print(number, digit_in_number, current_digit)

        # print("Digit {0} is {1}.".format(current, current_digit))
        # print()

        prod *= current_digit

    return prod


def parse_input():
    """
    parse hackerrank input
    https://www.hackerrank.com/contests/projecteuler/challenges/euler040
    """
    cases = int(input().strip())
    for _ in range(cases):
        indexes = [int(j) for j in input().strip().split(" ")]
        print(solve_problem(indexes))


def problem():
    """solve the project Euler problem"""
    print(solve_problem([1, 10, 100, 1000, 10000, 100000, 1000000]))


def debug_assertions():
    """unit tests"""
    assert solve_problem([1, 10, 100, 1000, 10000, 100000, 1000000]) == 210
    assert solve_problem([1, 2, 3, 4, 5, 6, 7]) == 5040


def main():
    """THE main"""
    debug_assertions()

    # parse_input()   # hackerrank
    problem()


if __name__ == "__main__":
    main()
