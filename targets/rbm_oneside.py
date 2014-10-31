import numpy as np
from expr.expr_matrix import ExprMatrix
from expr.expr_abstract import ExprAbstract
from targets.target import Target
import manage.config

class RBMOneSide(Target):
  def __init__(self, power):
    super(RBMOneSide, self).__init__()
    self.power = power
    self.complexity = 2
    self.Compute()

  def __str__(self):
    return "RBMOneSide%d" % self.power

  def Compute(self):
    n = 4
    m = 5
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
    for h_iter in range(0, pow(2, m)):
      row = []
      for mm in range(0, m):
        if h_iter & pow(2, mm):
          row.append([impl([1], np.array([zeros]))])
        else:
          row.append([impl([0], np.array([zeros]))])
      hs.append(ExprMatrix(comp="", \
        expressions=np.array(row), powers=powers))
    col = [impl([1], np.array([zeros]))] * n
    v = ExprMatrix(comp="", \
          expressions=np.array([col]), powers=powers)
    vW = v.Multiply(W)
    for h_iter in range(0, pow(2, m)):
      h = hs[h_iter]
      singles.append(vW.Multiply(h).Power(self.power))
    target = ExprAbstract.AddManyExpressions(singles)
    self.target_mat = target

