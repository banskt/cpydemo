import numpy as np
import argparse

from .stats import cmath

def parse_args():
    parser = argparse.ArgumentParser(description='csumpy: an example Python package with C libraries to sum two numbers')
    parser.add_argument('-a',
                        type = float,
                        dest = 'val_a',
                        metavar = 'FLOAT',
                        help = 'first number')
    parser.add_argument('-b',
                        type = float,
                        dest = 'val_b',
                        metavar = 'FLOAT',
                        help = 'second number')
    res = parser.parse_args()
    return res


def main():
    opts = parse_args()
    print (f"The input values are {opts.val_a} and {opts.val_b}")
    x = cmath.c_sum(opts.val_a, opts.val_b)
    print (f"Sum: {x}")
    y = cmath.c_diff(opts.val_a, opts.val_b)
    print (f"Diff: {y}")


if __name__ == "__main__":
    main()
