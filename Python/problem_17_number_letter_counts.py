"""
    Problem 17 : Number letter counts
    http://projecteuler.net/problem=17
        If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, \
        how many letters would be used?
    Version: 2016.05.03

    pylint--version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10 (previous run: 9.76/10, +0.24)

    TODO
    http://www.hackerrank.com/contests/projecteuler/challenges/euler017
        Difficulty: Easy
"""

def letters_no(number):
    """the number of letter for a given number"""
    no_letters = 0
    if number < 11:
        catalog = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        no_letters = len(catalog[number-1])
    elif number < 18:
        catalog = ["eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen"]
        no_letters = len(catalog[number-11])
    elif number < 21:
        catalog = ["eighteen", "nineteen", "twenty"]
        no_letters = len(catalog[number-18])
    elif number%10 == 0 and number < 100:
        catalog = ["thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        no_letters = len(catalog[number//10-3])
    elif number%100 == 0 and number < 1000:
        no_letters = letters_no(number//100) + len("hundred")
    elif number < 100:
        no_letters = letters_no(number//10*10) + letters_no(number%10)
    elif number < 1000:
        no_letters = letters_no(number//100*100) + letters_no(number%100) + len("and")
    elif number%1000 == 0 and number < 1000000:
        no_letters = letters_no(number//1000) + len("thousand")
    else:
        # above thousand is trickier because it has to have only one "and"
        assert False
    return no_letters

def count_letters_1(limit):
    """brute-force algorithm"""
    count = 0
    for year in range(1, 1+limit):
        count += letters_no(year)
    return count

def count_letters(limit):
    """solve the problem, print the needed time"""
    return count_letters_1(limit)

def debug_validations():
    """all the assertions"""
    assert count_letters(5) == 19
    assert letters_no(21) == 9
    assert letters_no(28) == 11
    assert letters_no(73) == 12
    assert letters_no(115) == 20
    assert letters_no(342) == 23
    assert letters_no(700) == 12
    assert count_letters(1000) == 21124

def main():
    """main function: defined explicitly for external calling"""
    debug_validations()
    print(count_letters(1000))

if __name__ == "__main__":
    main()
