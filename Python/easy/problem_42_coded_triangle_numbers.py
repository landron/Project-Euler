#! /usr/bin/python3
'''
    https://projecteuler.net/problem=42

    https://www.hackerrank.com/contests/projecteuler/challenges/euler042
        Score: 100.00

    "Your code has been rated at 10.00/10"
    pylint --version
        No config file found, using default configuration
        pylint 1.8.1,
        astroid 1.6.0
        Python 3.6.4
'''

import math

def get_triangular(nth):
    '''calculate nth triangular number'''
    return nth*(nth+1)//2

def create_triangulars():
    '''creates the triangulars cache used through this program'''
    triangulars = lambda: None
    triangulars.limit = 0
    triangulars.numbers = {}

    return triangulars

def is_number_triangular(number, triangulars): #pylint: disable=inconsistent-return-statements
    '''returns the generating number if triangular otherwise 0'''
    if number <= get_triangular(triangulars.limit):
        if number in triangulars.numbers:
            return triangulars.numbers[number]
        return 0

    while True:
        triangulars.limit += 1
        triangular = get_triangular(triangulars.limit)
        triangulars.numbers[triangular] = triangulars.limit

        if triangular == number:
            return triangulars.limit
        elif triangular > number:
            return 0

def is_number_triangular_simple(number):
    '''returns the generating number if triangular otherwise 0'''
    gen = math.floor(math.sqrt(2*number))
    # print(number, gen, get_triangular(gen))
    return gen if get_triangular(gen) == number else 0

def word_to_number(word):
    '''transforms a word in the equivalent number'''
    number = 0
    for _, char in enumerate(word):
        if ord(char) >= ord('A') and ord(char) <= ord('Z'):
            number += (ord(char)-ord('A')+1)
        elif ord(char) >= ord('a') and ord(char) <= ord('z'):
            number += (ord(char)-ord('a')+1)
    return number

def is_word_triangular(word, triangulars):
    '''returns the generating number if triangular otherwise 0'''
    return is_number_triangular(word_to_number(word), triangulars)

def parse_input():
    '''
        parse hackerrank input
        https://www.hackerrank.com/contests/projecteuler/challenges/euler042

        using create_triangulars => runtime error
            the numbers are too big
    '''

    cases = int(input().strip())
    for _ in range(cases):
        number = int(input().strip())
        gen = is_number_triangular_simple(number)
        if not gen:
            print(-1)
        else:
            print(gen)

def problem():
    '''solve the project Euler problem
        https://projecteuler.net/project/resources/p042_words.txt
    '''

    file = open('p042_words.txt', 'r')
    names_f = file.read()
    names = [i for i in names_f.strip('\" ').split('\",\"')]

    triangulars = create_triangulars()

    count = 0
    for i in names:
        if is_word_triangular(i, triangulars):
            count += 1
    print(count)

def debug_assertions():
    '''unit tests'''
    triangulars = create_triangulars()

    assert is_number_triangular(28, triangulars) == 7
    assert is_number_triangular(27, triangulars) == 0
    assert is_number_triangular(29, triangulars) == 0
    assert is_number_triangular(55, triangulars) == 10
    assert is_number_triangular(35, triangulars) == 0
    assert is_number_triangular(55, triangulars) == 10

    assert word_to_number('Sky') == 55
    assert is_word_triangular('Sky', triangulars) == 10

def main():
    '''THE main'''
    debug_assertions()

    # parse_input()   # hackerrank
    # problem()

if __name__ == "__main__":
    main()
