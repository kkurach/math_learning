import numpy as np
from expr.expr_matrix import ExprMatrix
from targets.target import Target
import manage.config
from manage.config import NUMPY, MATLAB, THEANO, THIS
import itertools

class RBMSparse(Target):
  def __init__(self, vsparse, hsparse=2):
    super(RBMSparse, self).__init__()
    self.vsparse = vsparse
    self.hsparse = hsparse
    self.complexity = 3
    self.Compute()

  def Compute(self):
    n = max(self.vsparse * self.hsparse, 2)
    m = n + 1
    manage.config.N, manage.config.M = n, m
    impl = manage.config.EXPR_IMPL
    manage.config.MAXPOWER = np.array([self.vsparse * self.hsparse])
    self.SetStartSymbols(1)
    target = None
    for v_iter in itertools.combinations(xrange(n), self.vsparse):
      for h_iter in itertools.combinations(xrange(m), self.hsparse):
        expr_vector = np.zeros((1, n * m))
        for v in v_iter:
          for h in h_iter:
            expr_vector[0, v * m + h] = 1
        expr = impl([1], expr_vector)
        if target is None:
          target = expr
        else:
          target = target + expr
    target = np.array([[target]])
    target = ExprMatrix(comp="", expressions=target, powers=manage.config.MAXPOWER)
    self.target_mat = target

  def __str__(self):
    return "RBMSparse%d" % self.vsparse
