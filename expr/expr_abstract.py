from fractions import gcd
from math import log
import manage.config
import numpy as np
import copy

class ExprAbstract(object):

  def __init__(self, quants, expr_vectors):
    assert len(quants) > 0
    assert type(expr_vectors) == np.ndarray
    assert expr_vectors.ndim == 2
    assert expr_vectors.shape[0] == len(quants)

    if all(q == 0 for q in quants):
      quants = [0]
      expr_vectors = np.array([expr_vectors[0]])
    self.quants = quants
    expr_vectors = expr_vectors.astype(np.int64)
    self.expr_vectors = expr_vectors

  def __mul__(self, other):
    raise Exception('Undefined operation mul')

  def __sub__(self, other):
    raise Exception('Undefined operation sub')

  def __add__(self, other):
    raise Exception('Undefined operation add')

  def __eq__(self, obj_expr_symbolic):
    raise Exception('Undefined operation eq')

  # Might be very slow.
  def __pow__(self, k):
    tmp = copy.copy(self)
    for _ in range(1, k):
      tmp = tmp.__mul__(self)
    return tmp

  @classmethod
  def SolutionStr(cls, weights, comps):
    print "cls", cls
    print "weights", weights
    print "comps", comps
    raise Exception('Undefined method SolutionStr')

  @classmethod
  def SolutionStrRBM(cls, weights, comps, deriv):
    from manage.config import NUMPY, THEANO, MATLAB, THIS
    n, m = manage.config.N, manage.config.M
    backs = [NUMPY, THEANO, MATLAB, THIS]
    print "weights", weights
    r = reduce(gcd, weights)
    r = abs(r)
    weights = [w / r for w in weights]
    result_strs = cls.SolutionStr(weights, comps)
    rc = gcd(r, 2 ** (n + m))
    r /= rc
    for b in backs:
      mult = "2**(n + m - %d) * %d" % (n + m - log(rc, 2), r)
      if deriv:
        result_strs[b] = "%s * (%s)" % (mult, result_strs[b])
      else:
        result_strs[b] = "%s * (%s)" % (mult, result_strs[b])
    return result_strs

  @staticmethod
  def AddManyExpressions(expr_list):
    assert len(expr_list) > 0
    while len(expr_list) > 1:
      list_new = []
      while True:
        if len(expr_list) == 0:
          break
        a = expr_list.pop(0)
        if len(expr_list) == 0:
          list_new.append(a)
          break
        b = expr_list.pop(0)
        list_new.append(a + b)
      expr_list = list_new
    return expr_list[0]

