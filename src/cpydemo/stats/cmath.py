import numpy as np
import ctypes
import sys
import os
import glob

def find_module_path(libname):
    for p in sys.path:
        if os.path.isdir(p) and any([x.startswith(libname) for x in os.listdir(p)]):
            return p
    

def c_sum(a, b):
    libname = 'cpydemo_sum_lib'
    _path = find_module_path(libname)
    clib = np.ctypeslib.load_library(libname, _path)
    csum = clib.sum
    csum.restype = ctypes.c_double
    csum.argtypes = [ctypes.c_double, ctypes.c_double]
    x = csum(a, b)
    return x


def c_diff(a, b):
    libname = 'cpydemo_diff_lib'
    _path = find_module_path(libname)
    clib = np.ctypeslib.load_library(libname, _path)
    cdiff = clib.diff
    cdiff.restype = ctypes.c_double
    cdiff.argtypes = [ctypes.c_double, ctypes.c_double]
    x = cdiff(a, b)
    return x
