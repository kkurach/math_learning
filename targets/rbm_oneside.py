import numpy as np
from expr.expr_matrix import ExprMatrix
from expr.expr_abstract import ExprAbstract
from targets.target import Target
import manage.config
from manage.config import MATLAB

class RBMOneSide(Target):
  def __init__(self, power):
    super(RBMOneSide, self).__init__()
    self.power = power
    self.complexity = 2
    self.Compute()

  def __str__(self):
    return "RBMOneSide%d" % self.power

  def Compute(self):
    n = 1
    m = max(self.power, 2) + 1
    manage.config.N, manage.config.M = n, m
    impl = manage.config.EXPR_IMPL
    manage.config.MAXPOWER = np.array([self.power])
    W = self.SetStartSymbols(1)[0]
    zeros = np.array([0] * (n * m))
    powers = [0]
    # Target expression: sum (v^T W)^k
    singles = []
    for h_iter in range(0, pow(2, m)):
      row = []
      for mm in range(0, m):
        if h_iter & pow(2, mm):
          row.append([impl([1], np.array([zeros]))])
        else:
          row.append([impl([0], np.array([zeros]))])
      h = ExprMatrix(comp="", \
        expressions=np.array(row), powers=powers)
      singles.append(W.Multiply(h).Power(self.power))
    target = ExprAbstract.AddManyExpressions(singles)
    matlab = '''n = 14;
m = 1;
A = randn(1, n);
nset = dec2bin(0:(2^(n) - 1));
original = 0;
for i = 1:size(nset, 1)
  v = logical(nset(i, :) - '0');
  original = original + (v * A') ^ %d;
end
''' % self.power
    target.comp[MATLAB] = matlab
 
    self.target_mat = target

