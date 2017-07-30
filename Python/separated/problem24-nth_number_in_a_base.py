#!/bin/python3
'''    
    https://projecteuler.net/problem=24
        https://www.hackerrank.com/contests/projecteuler/challenges/euler024
'''

import sys
import math

def find_next_unused_symbol(table, nth):
    for i in range(len(table)):
        if table[i]:
            continue
        if 0 == nth:
            table[i] = True
            return i
        nth -= 1
    return -1

def find_next_symbol(position, symbols, number):
    # print(position, number)

    if symbols.available == 0:
        digit = find_next_unused_symbol(symbols.used, 0)
        number += [digit]
        return

    quantity = symbols.factorials[len(symbols.factorials)-symbols.available]
    # print(position,quantity)

    digit = find_next_unused_symbol(symbols.used, position//quantity)
    assert digit != -1
    # print([digit])
    
    number += [digit]
    symbols.available -= 1

    find_next_symbol(position%quantity, symbols, number)

def find_nth_number(position, symbols_no):
    assert position != 0
    assert position <= math.factorial(symbols_no)

    symbols = lambda:None
    symbols.used = [False]*symbols_no
    symbols.factorials = []
    for i in range(symbols_no):
        symbols.factorials.append( math.factorial(symbols_no-i))
    symbols.available = symbols_no
    # print(symbols.factorials)

    # change position to 0-index
    position -= 1
    assert symbols.factorials[0] > position
    symbols.available -= 1

    number = [] 
    find_next_symbol(position, symbols, number)
    return number

# https://www.hackerrank.com/contests/projecteuler/challenges/euler024
def parse_input():
    T = int(input().strip())

    for _ in range(T):
        N = int(input().strip())
        number = find_nth_number(N, 13)

        str = ''
        for d in number:
            str += chr(ord('a')+d)
        print(str)

def project_euler():
    number = find_nth_number(1000000, 10)
    # print(number)
    str = ''
    for d in number:
        str += chr(ord('0')+d)
    print(str)

def debug_assertions():
    assert find_nth_number(1, 3) == [0, 1, 2]
    assert find_nth_number(2, 3) == [0, 2, 1]
    assert find_nth_number(3, 3) == [1, 0, 2]
    assert find_nth_number(4, 3) == [1, 2, 0]
    assert find_nth_number(5, 3) == [2, 0, 1]
    assert find_nth_number(6, 3) == [2, 1, 0]

def main():
    debug_assertions()
    project_euler()
    # parse_input()

if __name__ == "__main__":
    main()
