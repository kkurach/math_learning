import numpy as np
from expr.expr_matrix import ExprMatrix
from expr.expr_abstract import ExprAbstract
from targets.target import Target
import manage.config
from manage.config import MATLAB

class RBM(Target):
  def __init__(self, power):
    super(RBM, self).__init__()
    self.power = power
    self.complexity = 3
    self.Compute()

  def __str__(self):
    return "RBM%d" % self.power

  def Compute(self):
    n = max(self.power, 2)
    m = n + 1
    manage.config.N, manage.config.M = n, m
    impl = manage.config.EXPR_IMPL
    manage.config.MAXPOWER = np.array([self.power])
    W = self.SetStartSymbols(1)[0]
    zeros = np.array([0] * (n * m))
    powers = [0]
    # Target expression: sum (v^T W h)^k
    singles = []
    vs = []
    vWs = []
    hs = []
    for v_iter in range(0, pow(2, n)):
      col = []
      col01 = []
      for nn in range(0, n):
        if v_iter & pow(2, nn):
          col.append(impl([1], np.array([zeros])))
          col01.append(1)
        else:
          col.append(impl([0], np.array([zeros])))
          col01.append(0)
      v = ExprMatrix(comp="np.array([%s])" % str(col01), \
            expressions=np.array([col]), powers=powers)
      vs.append(v)
      vWs.append(v.Multiply(W))
    for h_iter in range(0, pow(2, m)):
      row = []
      row01 = []
      for mm in range(0, m):
        if h_iter & pow(2, mm):
          row.append([impl([1], np.array([zeros]))])
          row01.append(1)
        else:
          row.append([impl([0], np.array([zeros]))])
          row01.append(0)
      hs.append(ExprMatrix(comp="np.array([%s]).transpose()" % str(row01), \
        expressions=np.array(row), powers=powers))
    for v_iter in range(0, pow(2, n)):
      v = vs[v_iter]
      vW = vWs[v_iter]
      for h_iter in range(0, pow(2, m)):
        h = hs[h_iter]
        singles.append(vW.Multiply(h).Power(self.power))
    target = ExprAbstract.AddManyExpressions(singles)
    matlab = '''n = 7;
m = 8;
A = randn(n, m);
nset = dec2bin(0:(2^(n) - 1));
mset = dec2bin(0:(2^(m) - 1));
original = 0;
for i = 1:size(nset, 1)
  for j = 1:size(mset, 1)
    v = logical(nset(i, :) - '0');
    h = logical(mset(j, :) - '0');
    original = original + (v * A * h') ^ %d;
  end
end
''' % self.power
    target.comp[MATLAB] = matlab

    self.target_mat = target

