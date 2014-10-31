import numpy as np
import manage.config
from expr import expr_common
from fractions import Fraction as F

class Solver(object):
  def __init__(self):
    pass

  @staticmethod
  def GaussP(A, b):
    A = A.astype(np.int64)
    b = b.astype(np.int64)
    A = np.rint(A)
    b = np.rint(b)
    m = A.shape[0]
    n = A.shape[1]
    r = 0
    q = []
    P = long(manage.config.PRIME)
    for k in xrange(min(m, n)):
      r = k + 1
      nonzero_j = None
      nonzero_i = None
      for iter_j in xrange(k, n):
        for iter_i in xrange(k, m):
          if A[iter_i, iter_j] % P != 0 and nonzero_i is None:
            nonzero_i = iter_i
            nonzero_j = iter_j

      if nonzero_i is None:
        r = k
        break
      if nonzero_j != k:
        for t in xrange(m):
          A[t, nonzero_j], A[t, k] = A[t, k], A[t, nonzero_j]
      q.append(nonzero_j)
      if nonzero_i != k:
        b[nonzero_i], b[k] = b[k], b[nonzero_i]
        for t in xrange(n):
          A[nonzero_i, t], A[k, t] = A[k, t], A[nonzero_i, t]

      for j in xrange(k + 1, m):
        if A[j, k] == -P or A[j, k] == P:
          A[j, k] = 0
        if A[j, k] != 0:
          l = (A[j, k] * expr_common.RevMod(A[k, k], P)) % P
          for i in xrange(k+1, n):
            A[j, i] = (A[j, i] - (l * A[k, i]) % P) % P
          b[j] = (b[j] - (l * b[k]) % P) % P
    # r is a rank of matrix A
    x = [0] * n
    for k in xrange(r, m):
      if b[k] != 0 and b[k] != P and b[k] != -P:
        return []
    for k in xrange(r - 1, -1, -1):
      s = b[k]
      for j in xrange(k + 1, r):
        s = (P + s - (A[k, j] * x[j]) % P) % P
      x[k] = (s * expr_common.RevMod(A[k, k], P)) % P
    for k in xrange(r - 1, -1, -1):
      x[k], x[q[k]] = x[q[k]], x[k]
    return x

  @staticmethod
  def GaussF(A, b):
    m = A.shape[0]
    n = A.shape[1]
    print "A.shape:", A.shape
    print "b.shape:", b.shape
    r = 0
    q = []
    for k in xrange(min(m, n)):
      r = k + 1
      nonzero_j = None
      nonzero_i = None
      for iter_j in xrange(k, n):
        for iter_i in xrange(k, m):
          if A[iter_i, iter_j] != 0 and nonzero_i is None:
            nonzero_i = iter_i
            nonzero_j = iter_j

      if nonzero_i is None:
        r = k
        break
      if nonzero_j != k:
        for t in xrange(m):
          A[t, nonzero_j], A[t, k] = A[t, k], A[t, nonzero_j]
      q.append(nonzero_j)
      if nonzero_i != k:
        b[nonzero_i], b[k] = b[k], b[nonzero_i]
        for t in xrange(n):
          A[nonzero_i, t], A[k, t] = A[k, t], A[nonzero_i, t]

      for j in xrange(k + 1, m):
        if A[j, k] != 0:
          l = A[j, k] / A[k, k]
          for i in xrange(k+1, n):
            A[j, i] = A[j, i] - l * A[k, i]
          b[j] = b[j] - l * b[k]
    # r is a rank of matrix A
    x = np.vectorize(F)(np.zeros(n))
    for k in xrange(r, m):
      if b[k] != 0:
        return []
    for k in xrange(r - 1, -1, -1):
      s = b[k]
      for j in xrange(k + 1, r):
        s = s - A[k, j] * x[j]
      x[k] = s / A[k, k]
    for k in xrange(r - 1, -1, -1):
      x[k], x[q[k]] = x[q[k]], x[k]
    return x


