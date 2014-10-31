import numpy as np
from expr.expr_matrix import ExprMatrix
import manage.config

def GetMatricesSumMul(n, m, expr_impl):
  manage.config.MAXPOWER = np.array([10, 10])
  mat_a = []
  for r in xrange(n):
    row = []
    for c in xrange(m):
      vec = [0] * (2 * n * m)
      vec[r * m + c] = 1
      row.append(expr_impl([1], np.array([vec])))
    mat_a.append(row)
  mat_b = []
  for r in xrange(n):
    row = []
    for c in xrange(m):
      vec = [0] * (2 * n * m)
      vec[n * m + r * n + c] = 1
      row.append(expr_impl([1], np.array([vec])))
    mat_b.append(row)

  A = ExprMatrix(comp='A',
                 expressions=np.array(mat_a),
                 powers=np.array([1, 0]))
  B = ExprMatrix(comp='B',
                 expressions=np.array(mat_b),
                 powers=np.array([0, 1]))
  return A, B

