import os
import unittest
import scipy.stats as sc_stats

from cpydemo.stats import cmath
from cpydemo.utils.logs import MyLogger

mlogger = MyLogger(__name__)

class TestCPyDemo(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestCPyDemo, self).__init__(*args, **kwargs)
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


if __name__ == '__main__':
    unittest.main()
