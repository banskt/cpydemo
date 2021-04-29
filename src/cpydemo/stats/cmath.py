import numpy as np
import ctypes
import sys
import os
import glob

def find_module_path(libname):
    for p in sys.path:
        if os.path.isdir(p) and any([x.startswith(libname) for x in os.listdir(p)]):
            return p


def get_clib(cname):
    libprefix = 'libcpydemo'
    libname = '{:s}_{:s}'.format(libprefix, cname)
    _path = find_module_path(libname)
    clib = np.ctypeslib.load_library(libname, _path)
    return clib
    

def c_sum(a, b):
    csum = get_clib('sum').sum
    csum.restype = ctypes.c_double
    csum.argtypes = [ctypes.c_double, ctypes.c_double]
    x = csum(a, b)
    return x


def c_diff(a, b):
    cdiff = get_clib('diff').diff
    cdiff.restype = ctypes.c_double
    cdiff.argtypes = [ctypes.c_double, ctypes.c_double]
    x = cdiff(a, b)
    return x


def c_pval(x, mu, sigma):
    cpval = get_clib('one_sided_pval').one_sided_pval
    cpval.restype = ctypes.c_double
    cpval.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
    p = cpval(x, mu, sigma)
    return p


def c_matmul(X, Y):
    cmatmul = get_clib('matmul').matmulAB
    cmatmul.restype = ctypes.c_bool
    cmatmul.argtypes = [
        np.ctypeslib.ndpointer(ctypes.c_double, ndim=1, flags='C_CONTIGUOUS, ALIGNED'),
        np.ctypeslib.ndpointer(ctypes.c_double, ndim=1, flags='C_CONTIGUOUS, ALIGNED'),
        np.ctypeslib.ndpointer(ctypes.c_double, ndim=1, flags='C_CONTIGUOUS, ALIGNED'),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    m, k = X.shape
    k, n = Y.shape
    assert X.shape[1] == Y.shape[0], "Incorrect dimensions for matrix multiplication"
    Z = np.zeros((m, n))
    success = cmatmul(X.reshape(-1), Y.reshape(-1), Z.reshape(-1), m, k, n)
    return Z.reshape(m, n)


def c_svd(X):
    csvd = get_clib('svd').svd
    csvd.restype = ctypes.c_bool
    csvd.argtypes = [
        np.ctypeslib.ndpointer(ctypes.c_double, ndim=1, flags='C_CONTIGUOUS, ALIGNED'),
        np.ctypeslib.ndpointer(ctypes.c_double, ndim=1, flags='C_CONTIGUOUS, ALIGNED'),
        np.ctypeslib.ndpointer(ctypes.c_double, ndim=1, flags='C_CONTIGUOUS, ALIGNED'),
        np.ctypeslib.ndpointer(ctypes.c_double, ndim=1, flags='C_CONTIGUOUS, ALIGNED'),
        ctypes.c_int,
        ctypes.c_int,
    ]
    m, n = X.shape
    k = min(m, n)
    cX = X.copy().reshape(-1)
    cS = np.zeros(k).reshape(-1)
    cU = np.zeros((m, k)).reshape(-1)
    cVT = np.zeros((k, n)).reshape(-1)
    success = csvd(cX, cS, cU, cVT, m, n)

    return cU.reshape(m, k), cS, cVT.reshape(k, n)
