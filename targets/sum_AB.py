import numpy as np
from targets.target import Target
import copy
import manage.config
from math import floor, ceil
from manage.config import MATLAB

class SumAB(Target):

  def __init__(self, k=2):
    super(SumAB, self).__init__()
    if k == 0:
      k = 1
    self.k = k
    self.Compute()

  def Compute(self):
    n, m = 5, 6
    manage.config.N, manage.config.M = n, m
    manage.config.MAXPOWER = np.array([ceil(float(self.k) / 2.), floor(float(self.k) / 2.)])
    A, B = self.SetStartSymbolsWithShapes([(n, m), (m, n)])
    target = copy.copy(A)
    for i in xrange(self.k - 1):
      if i % 2 == 0:
        target = target.Multiply(B)
      else:
        target = target.Multiply(A)

    target = target.Marginalize(axis=None)
    target.comp[MATLAB] = "n = 100;\nm = 200;\nA = randn(n, m);\nB = randn(m, n);\noriginal = " + target.comp[MATLAB] + ";\n"
    self.target_mat = target

  def __str__(self):
    return "SumAAT%d" % self.k
