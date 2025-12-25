#!/bin/python3
"""
tag_point
tag_python_class, tag_python_class_operators, tag_python_equality

Usage
    https://github.com/landron/Problems/blob/public-master/hackerrank/algo/Graph%20Theory/rook_shortest_path.py

flake8, pylint
"""


class Point:
    """a 2D point"""

    # pylint: disable=invalid-name  # needed for x,y,pt

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __str__(self):
        if not self:
            return "Undefined point"
        if isinstance(self.x, int) and isinstance(self.y, int):
            return f"({self.x},{self.y})"
        return f"({self.x:.2f},{self.y:.2f})"

    def __bool__(self):
        """
        return self.x and self.y
            TypeError: __bool__ should return bool, returned NoneType
        !!! only None
        """
        return self.x is not None and self.y is not None

    def __eq__(self, other):
        """why is this necessary ?

        https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
        """
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def advance_if(self, x, y, limit_x, limit_y):
        """can the point be updated in the new given direction ?"""
        if x == y == 0:
            return False
        x_new = self.x + x
        y_new = self.y + y

        def good_coord(cols, rows, x, y):
            if x < 0 or y < 0:
                return False
            if rows <= x or cols <= y:
                return False
            return True

        if not good_coord(limit_x, limit_y, x_new, y_new):
            return Point()

        return Point(x_new, y_new)


def debug_assertions():
    """
    unit tests, assertions
    """
    pt1 = Point()
    assert not pt1
    pt2 = Point(1, 2)
    assert pt2
    assert pt2 != pt1
    pt3 = Point(1, 2)
    assert pt2 != pt1
    assert pt3 == pt2
    assert str(pt3) == "(1,2)"


def main():
    """main"""
    debug_assertions()


if __name__ == "__main__":
    main()
