import numpy as np
from targets.target import Target
import copy
import manage.config
from math import floor, ceil

class SumAB(Target):

  def __init__(self, k=2):
    super(SumAB, self).__init__()
    if k == 0:
      k = 1
    self.k = k
    self.Compute()

  def Compute(self):
    n, m = 2, 3
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
    self.target_mat = target

  def __str__(self):
    return "SumAAT%d" % self.k
