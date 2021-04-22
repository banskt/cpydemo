import numpy as np
import ctypes
import sys
import os
import glob

def find_module_path(libname):
    for p in sys.path:
        if os.path.isdir(p) and any([x.startswith(libname) for x in os.listdir(p)]):
            return p


def get_clib(libname):
    _path = find_module_path(libname)
    clib = np.ctypeslib.load_library(libname, _path)
    return clib
    

def c_sum(a, b):
    csum = get_clib('cpydemo_sum_lib').sum
    csum.restype = ctypes.c_double
    csum.argtypes = [ctypes.c_double, ctypes.c_double]
    x = csum(a, b)
    return x


def c_diff(a, b):
    cdiff = get_clib('cpydemo_diff_lib').diff
    cdiff.restype = ctypes.c_double
    cdiff.argtypes = [ctypes.c_double, ctypes.c_double]
    x = cdiff(a, b)
    return x


def c_pval(x, mu, sigma):
    cpval = get_clib('cpydemo_one_sided_pval_lib').one_sided_pval
    cpval.restype = ctypes.c_double
    cpval.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
    p = cpval(x, mu, sigma)
    return p

