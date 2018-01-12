import argparse
import sys
import collections


def print_row(row):
    for val in row:
        print(val, end=' ')
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of vertices in generated cycle')
    args = parser.parse_args()

    if args.n < 3:
        print('N must be >= 3')
        return 1

    row = collections.deque()
    row.extend([1, 0, 1])
    row.extend([0 for _ in range(3, args.n)])
    row.rotate(-1)

    for _ in range(args.n):
        print_row(row)
        row.rotate(1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
