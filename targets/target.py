import numpy as np
from expr.expr_matrix import ExprMatrix
import manage.config

class Target(object):

  def __init__(self):
    self.start_symbols = []
    self.maxpower = None
    self.complexity = 2
    self.target_mat = None

  def SetStartSymbols(self, nr):
    n, m = manage.config.N, manage.config.M
    self.start_symbols = []
    for k in range(nr):
      mat = []
      for r in xrange(n):
        row = []
        for c in xrange(m):
          vec = np.array([0] * nr * (n * m))
          vec[k * n * m + r * m + c] = 1
          row.append(manage.config.EXPR_IMPL([1], np.array([vec])))
        mat.append(row)
      powers = np.array([0] * nr)
      powers[k] = 1
      expr_mat = ExprMatrix(
          comp=chr(ord('A') + k),
          expressions=np.array(mat),
          powers=powers)
      self.start_symbols.append(expr_mat)
    return self.start_symbols

  def SetStartSymbolsWithShapes(self, mat_shapes):
    self.start_symbols = []
    total_variables = sum(n * m for n, m in mat_shapes)
    variables_so_far = 0
    for k, (n, m) in enumerate(mat_shapes):
      mat = []
      for r in xrange(n):
        row = []
        for c in xrange(m):
          vec = np.array([0] * total_variables)
          vec[variables_so_far + r * m + c] = 1
          row.append(manage.config.EXPR_IMPL([1], np.array([vec])))
        mat.append(row)
      powers = np.array([0] * len(mat_shapes))
      powers[k] = 1
      expr_mat = ExprMatrix(
          comp=chr(ord('A') + k),
          expressions=np.array(mat),
          powers=powers)
      self.start_symbols.append(expr_mat)
      variables_so_far += n * m
    assert variables_so_far == total_variables
    return self.start_symbols

  def GetStartSymbols(self):
    return self.start_symbols

  def GetTargetExpression(self):
    return self.target_mat
