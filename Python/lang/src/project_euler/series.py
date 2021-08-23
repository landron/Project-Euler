'''
    Ordered series of numbers
'''
from functools import total_ordering
import bisect


@total_ordering
class Series:
    '''
        ordered series of numbers
    '''
    def __init__(self, numbers=None):
        if isinstance(numbers, int):
            self.digits = [numbers]
        elif isinstance(numbers, list):
            self.digits = sorted(numbers)
        elif isinstance(numbers, Series):
            self.digits = numbers.digits[:]
        else:
            self.digits = []

    def __eq__(self, other):
        if len(self.digits) != len(other.digits):
            return False
        for i, val in enumerate(self.digits):
            if val != other.digits[i]:
                return False
        return True

    def __lt__(self, other):
        if len(self.digits) != len(other.digits):
            return len(self.digits) < len(other.digits)
        for i, val in enumerate(self.digits):
            if val != other.digits[i]:
                return val < other.digits[i]
        return False

    def __repr__(self):
        as_str = ''
        j = -1
        for i, val in enumerate(self.digits):
            if val > 9:
                j = i
                break
            as_str += str(val)
        if j != -1:
            for i in range(j, len(self.digits)):
                as_str += ' '
                val = self.digits[i]
                as_str += str(val)
        return as_str

    def add(self, number):
        '''
            add a number to the series
        '''
        bisect.insort_left(self.digits, number)
        return self

    def new(self, number):
        '''
            add a number to NEW series
        '''
        copy = Series(self)
        return copy.add(number)

    @staticmethod
    def contains(series, item):
        '''
            does the given list contains the given Series ?
        '''
        where = bisect.bisect_left(series, item)
        return where != len(series) and series[where] == item

    @staticmethod
    def insert(series, item):
        '''
            does the given list contains the given Series ?
        '''
        if not Series.contains(series, item):
            bisect.insort_left(series, item)


def debug_assertions():
    '''
        unit tests for Series
    '''
    assert not str(Series())
    assert str(Series(3)) == '3'
    assert str(Series([3, 1, 2])) == '123'
    assert str(Series([11, 111, 1])) == '1 11 111'
    assert str(Series([8, 3, 1]).add(7)) == '1378'
    assert str(Series([8, 3, 1]).new(7)) == '1378'
    assert str(Series([10, 3, 1]).add(7)) == '137 10'

    series = []
    for i in [1111, 13, 112]:
        Series.insert(series, Series(i))
    for i in [1111, 13, 112]:
        Series.insert(series, Series(i))
    assert len(series) == 3
    for i in [1111, 13, 112]:
        assert Series.contains(series, Series(i))


def main():
    '''main'''
    debug_assertions()


if __name__ == "__main__":
    main()
