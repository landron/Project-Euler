#! /usr/bin/python3


def solve(func):
    '''solve the problem getting text using the given function'''

    trips = int(func().strip())
    for _ in range(trips):
        (n, c, m) = [int(j) for j in func().strip().split(' ')]
        total = n//c
        no = total
        print(total)
        while no >= m:
            next = no//m
            no -= m*next
            no += next
            total += next
        print(total)


def process_test(input_func, output):
    _, div = map(int, input_func().strip().split())
    data = list(map(int, input_func().rstrip().split()))
    print(div, data)

    result = 0
    output.write(result + '\n')


def process_input():
    fptr = open('output.txt', 'w')
    f2 = open('input09.txt', 'r')

    process_test(f2.readline, fptr)

    f2.close()
    fptr.close()


def main():
    solve(input)


if __name__ == "__main__":
    main()
