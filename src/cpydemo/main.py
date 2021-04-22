import numpy as np
import argparse
import sys
import unittest

from .stats import cmath
from .utils.logs import MyLogger
from tests_cpydemo.test_cpydemo import TestCPyDemo

mlogger = MyLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='CPyDemo: demonstration of packaging a command line tool written in Python and C using MKL and mpi4py')
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
    parser.add_argument('--test',
                        dest = 'test',
                        action='store_true',
                        help='Perform unit tests')
    res = parser.parse_args()
    return res


def target(opts):
    print (f"The input values are {opts.val_a} and {opts.val_b}")
    x = cmath.c_sum(opts.val_a, opts.val_b)
    print (f"Sum: {x}")
    y = cmath.c_diff(opts.val_a, opts.val_b)
    print (f"Diff: {y}")
    return


def run_unittests():
    mlogger.info("Running tests")
    test_classes = [TestCPyDemo]
    loader = unittest.TestLoader()
    test_list = [loader.loadTestsFromTestCase(tclass) for tclass in test_classes]
    test_suite = unittest.TestSuite(test_list)
    runner = unittest.TextTestRunner()
    results = runner.run(test_suite)
    return
    

def main():
    opts = parse_args()
    if opts.test:
        run_unittests()
    else:
        target(opts)


if __name__ == "__main__":
    main()
