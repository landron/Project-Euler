#!/bin/python3
"""
https://projecteuler.net/problem=22
    https://www.hackerrank.com/contests/projecteuler/challenges/euler022
"""

import sys


def score(name):
    sum = 0
    for ch in name:
        sum += ord(ch) - ord("A") + 1
    return sum


# https://www.hackerrank.com/contests/projecteuler/challenges/euler022
def parse_lines():
    N = int(input().strip())
    names = [""] * N
    for i in range(N):
        names[i] = input().strip()
    # print(names)
    names.sort()
    Q = int(input().strip())
    for _ in range(Q):
        name = input().strip()
        print((1 + names.index(name)) * score(name))


def sum_of_names(names_in):
    names = sorted(names_in)

    # print(names)
    # print(names[0], names[1], names[-1])

    sum = 0
    for i in range(len(names)):
        sum += (i + 1) * score(names[i])
    return sum


def debug_assertions():
    assert score("COLIN") == 53
    assert score("PAMELA") == 48


def parse_names_file(names_file):
    f = open(names_file, "r")
    names_f = f.read()
    names = [i for i in names_f.strip('" ').split('","')]

    result = sum_of_names(names)
    print(result)


def main():
    debug_assertions()
    parse_names_file("p022_names.txt")
    # parse_lines()


if __name__ == "__main__":
    main()
