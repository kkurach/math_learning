import numpy as np
from expr.expr_matrix import ExprMatrix
from expr.expr_abstract import ExprAbstract
from targets.target import Target
import manage.config
import itertools

class Sym(Target):
  def __init__(self, power):
    super(Sym, self).__init__()
    self.power = power
    self.complexity = 2
    self.Compute()

  def __str__(self):
    return "Sym%d" % self.power

  def Compute(self):
    n = 1
    m = max(self.power, 3) + 3
    manage.config.N, manage.config.M = n, m
    impl = manage.config.EXPR_IMPL
    manage.config.MAXPOWER = np.array([self.power])
    self.SetStartSymbols(1)
    target = None
    for h_iter in itertools.combinations(xrange(m), self.power):
      small_target = None
      expr_vector = np.zeros((1, m))
      for h in h_iter:
        expr_vector[0, h] = 1
      expr = impl([1], expr_vector)
      if target is None:
        target = expr
      else:
        target = target + expr
    target = np.array([[target]])
    target = ExprMatrix(comp="", expressions=target, powers=manage.config.MAXPOWER)
    self.target_mat = target
