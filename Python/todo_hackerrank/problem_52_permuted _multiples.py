#!/bin/python3
'''
    https://projecteuler.net/problem=52
        Permuted multiples

    https://www.hackerrank.com/contests/projecteuler/challenges/euler052
        todo_hackerrank:
            55.56 (4/9 timeouts: 5,6,7,8)

            77.78 (2/9 timeouts: 5,6)
                use direct numbers multiplications (has_permuted_multiples_2) \
                    instead of digits operation (has_permuted_multiples)

            88.89 (timeout: 6)
                iterator wrongly used a second time

    pylint 1.8.1
        Your code has been rated at 8.62/10.

    tag_digits
'''

from proj_euler import get_digits

def multiply(digits, mul, pass_allowed=False):
    size = len(digits)
    result = [0]*size

    reminder = 0
    for i in range(size):
        val = mul*digits[i] + reminder
        result[i] = val%10
        reminder = val//10

    if reminder != 0:
        if not pass_allowed:
            return []
        result.insert(0, reminder)

    return result

def is_zero(list_in):
    for i in list_in:
        if i:
            return False
    return True

def same_digits_hash(hash_digits, number2):
    for i in number2:
        if hash_digits[i] == 0:
            return False
        hash_digits[i] -= 1

    return is_zero(hash_digits)

def same_digits(number1, number2):
    size = len(number1)
    assert len(number2) == size

    found = [0]*10
    for i in number1:
        found[i] += 1
    return same_digits_hash(found, number2)

def has_permuted_multiples(number, max_multiplier):
    digits = get_digits(number)
    # -1 : skip 1
    for i in range(max_multiplier-1):
        mul = multiply(digits, max_multiplier-i)
        if not mul or not same_digits(mul, digits):
            return False
    return True

def has_permuted_multiples_2(number, max_multiplier):
    digits = get_digits(number)
    found = [0]*10

    # -1 : skip 1
    for i in range(max_multiplier-1):
        # hackerrank - starting with the greatest matters: one test passed
        mul = number * (max_multiplier-i)
        digits_2 = get_digits(mul)

        if len(digits_2) > len(digits):
            return False

        assert is_zero(found)
        for j in digits:
            found[j] += 1
        if not same_digits_hash(found, digits_2):
            return False

    return True

def solve_problem():
    i = 1
    while not has_permuted_multiples(i, 6):
        i += 1
        # if 0 == i % 1000:
        #     print(i)
    return i

def get_all(limit, max_multiplier):
    '''
        hackerrank conditions
    '''
    result = []

    i = 1
    while i < limit:
        # if has_permuted_multiples(i, max_multiplier):
        if has_permuted_multiples_2(i, max_multiplier):
            result.append(i)
        i += 1

    return result

def parse_input():
    '''
        https://www.hackerrank.com/contests/projecteuler/challenges/euler052
    '''
    (N, K) = (int(i) for i in input().strip().split(' '))
    result = get_all(N, K)
    for i in result:
        show = ''
        for j in range(K):
            show += str((j+1)*i)
            show += ' '
        print(show)

def problem():
    return solve_problem()

def debug_assertions():
    assert get_digits(125874) == [4, 7, 8, 5, 2, 1]
    assert multiply([4, 7, 8, 5, 2, 1], 2) == [8, 4, 7, 1, 5, 2]
    assert same_digits([8, 4, 7, 1, 5, 2], [4, 7, 8, 5, 2, 1])
    assert not same_digits([8, 4, 7, 1, 5, 2, 2], [4, 7, 8, 5, 2, 1, 1])

def main():
    debug_assertions()

    # parse_input()
    print(problem())

if __name__ == "__main__":
    main()
