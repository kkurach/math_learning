import numpy as np
from expr.expr_matrix import ExprMatrix
from expr.expr_abstract import ExprAbstract
from targets.target import Target
import manage.config
from manage.config import MATLAB, THIS
import math
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
    m = max(self.power, 3) + 7
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
    matlab = '''n = 1;
m = 18;
A = randn(1, m);
sub = nchoosek(1:m, %s);
original = 0;
for i = 1:size(sub, 1)
  original = original + prod(A(sub(i, :)));
end
''' % self.power
    target = ExprMatrix(comp={THIS: ""}, expressions=target, powers=manage.config.MAXPOWER)
    target = target.ElementwiseMultiply(120)
    target.comp[MATLAB] = matlab
    self.target_mat = target
