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


if __name__ == '__main__':
    tester.main()
