import os
import unittest
import scipy.stats as sc_stats
import numpy as np

from cpydemo.stats import cmath
from cpydemo.utils.logs import MyLogger
import cpydemo.unittest_tester as tester

mlogger = MyLogger(__name__)

class TestCMath(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestCMath, self).__init__(*args, **kwargs)
        self.a = 3.5
        self.b = 2.4


    def test_csum(self):
        x = cmath.c_sum(self.a, self.b)
        mlogger.info(f"{self.a} + {self.b} = {x}")
        self.assertAlmostEqual(x, self.a + self.b, places = 3, msg = "Error in cmath.c_sum")


    def test_cdiff(self):
        x = cmath.c_diff(self.a, self.b)
        mlogger.info(f"{self.a} - {self.b} = {x}")
        self.assertAlmostEqual(x, self.a - self.b, places = 3, msg = "Error in cmath.c_diff")


    def test_pval(self):
        mu = 1.0
        sigma = 2.0
        val = 5.3
        x = cmath.c_pval(val, mu, sigma)
        mlogger.info(f"p-value of {val} with a null hypothesis of N({mu}, {sigma**2}) = {x}")
        scaled_val = (val - mu) / sigma
        p = 1 - sc_stats.norm.cdf(scaled_val)
        self.assertAlmostEqual(x, p, places = 3, msg = "Error in cmath.c_pval")


    def test_matmul(self):
        m = 100
        k = 80
        n = 200
        A = np.random.normal(0, 1, size = m * k).reshape(m, k)
        B = np.random.normal(0, 1, size = k * n).reshape(k, n)
        C = cmath.c_matmul(A, B)
        Ctrue = np.dot(A, B)
        self.assertTrue(np.allclose(C, Ctrue), msg = "Matrix multiplication do not match numpy")
        mlogger.info("Matrix multiplication successful")


    def test_svd(self):
        m = 4
        n = 3
        A = np.random.normal(0, 1, size = m * n).reshape(m, n)
        np_U, np_S, np_VT = np.linalg.svd(A, full_matrices = False)
        U, S, VT = cmath.c_svd(A)
        check_sv = np.allclose(S, np_S)
        check_reconstruct = np.allclose(A, np.dot(U, np.dot(np.diag(S), VT)))
        self.assertTrue(check_sv, msg = "SVD do not match numpy.linalg.svd")
        self.assertTrue(check_reconstruct, msg = "SVD from C cannot reconstruct original matrix")
        mlogger.info("SVD successful")


if __name__ == '__main__':
    tester.main()
