import numpy as np
from targets.target import Target
import copy
import manage.config
from manage.config import MATLAB

class SumAAT(Target):

  def __init__(self, k=2):
    super(SumAAT, self).__init__()
    if k == 0:
      k = 1
    self.k = k
    self.Compute()

  def Compute(self):
    manage.config.N, manage.config.M = 5, 6
    manage.config.MAXPOWER = np.array([self.k])
    [A] = self.SetStartSymbols(1)
    aT = A.Transpose()
    target = copy.copy(A)
    for i in xrange(self.k - 1):
      if i % 2 == 0:
        target = target.Multiply(aT)
      else:
        target = target.Multiply(A)
    target = target.Marginalize(axis=None)
    target.comp[MATLAB] = "n = 100;\nm = 200;\nA = randn(n, m);\noriginal = " + target.comp[MATLAB] + ";\n"
    self.target_mat = target

  def __str__(self):
    return "SumAAT%d" % self.k
