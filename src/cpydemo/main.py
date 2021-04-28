import numpy as np
import argparse
import sys
import unittest
import mpi4py
mpi4py.rc.initialize = False
mpi4py.rc.finalize = False
from mpi4py import MPI

from .stats import cmath
from .utils.logs import MyLogger
from .stats.tests.test_cmath import TestCMath
from cpydemo.unittest_tester import UnittestTester

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
    tester = UnittestTester(TestCMath)
    tester.execute()
    del tester
    return


def main():

    MPI.Init()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    ncore = comm.Get_size()

    if rank == 0:
        mlogger.info("Using MPI in {:d} cores".format(ncore))
        opts = parse_args()
    else:
        mlogger.info("Reporting from node {:d}".format(rank))
        opts = None

    opts = comm.bcast(opts, root = 0)
    comm.barrier()
    if rank != 0:
        option_string = ', '.join([f'{k}: {v}' for k, v in vars(opts).items()])
        mlogger.info("Node {:d}, Options: {:s}".format(rank, option_string))

    if rank == 0:
        if opts.test:
            run_unittests()
        else:
            target(opts)
    MPI.Finalize()


if __name__ == "__main__":
    main()
