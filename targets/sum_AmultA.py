import numpy as np
from targets.target import Target
import copy
import manage.config

class SumAmultA(Target):

  def __init__(self, k=2):
    super(SumAmultA, self).__init__()
    if k == 0:
      k = 1
    self.k = k
    self.complexity = 2
    self.Compute()

  def Compute(self):
    manage.config.N, manage.config.M = 2, 3
    manage.config.MAXPOWER = np.array([1000])
    [A] = self.SetStartSymbols(1)
    aT = A.Transpose()
    A2 = A.ElementwiseMultiply(A)
    target = copy.copy(A)
    power = 1
    for i in xrange(self.k - 1):
      if i % 2 == 0:
        target = target.Multiply(aT)
        power += 1
      else:
        target = target.Multiply(A2)
        power += 2
    target = target.Marginalize(axis=None)
    self.target_mat = target
    manage.config.MAXPOWER = np.array([power])

  def __str__(self):
    return "SumAmultA%d" % self.k
