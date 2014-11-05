import numpy as np
import manage.config
from manage.config import PRIME, NUM_EVAL, NUM_HASH
from manage import solver
import expr.expr_abstract as expr_abstract
import expr.expr_common as expr_common
import copy
from fractions import Fraction as F
from fractions import gcd

class ExprZp(expr_abstract.ExprAbstract):
  # expr vectors should be a list of vectors representing variables
  def __init__(self, quants=None, expr_vectors=None):
    def hash_mapping((quant, expr_vector)):
      rand_vals = expr_common.GetRandVals()
      quant = long(quant)
      s = np.ones(NUM_EVAL, dtype=np.int64)
      assert expr_vector.ndim == 1
      for i in xrange(len(expr_vector)):
        s = (s * rand_vals[:NUM_EVAL, i, expr_vector[i]]) % PRIME
      return (s * quant) % PRIME

    if quants is None and expr_vectors is None:
      return # TODO(karol): create builder function
    super(ExprZp, self).__init__(quants, expr_vectors)
    self.expr = np.zeros(NUM_EVAL, dtype=np.int64)
    self.expr = np.vectorize(long)(self.expr)
    ss = map(hash_mapping, zip(self.quants, self.expr_vectors))
    for s in ss:
      self.expr = (self.expr + s) % PRIME

  def __add__(self, other):
    c = ExprZp()
    c.expr = (self.expr + other.expr) % PRIME
    return c

  def __sub__(self, other):
    c = ExprZp()
    c.expr = (self.expr - other.expr) % PRIME
    return c

  def __mul__(self, other):
    c = ExprZp()
    if isinstance(other, (int, long, float, np.int64, F)):
      c.expr = (self.expr * other) % PRIME
    else:
      c.expr = (self.expr * other.expr) % PRIME
    return c

  def Hash(self):
    return self.expr[0:NUM_HASH]

  def __eq__(self, other):
    return (self.Hash() == other.Hash()).all()

  def DebugString(self):
    l = self.expr.shape[0]
    return 'Zp:' + str(self.expr[0:min(l, 2)]) + "..."

  def PrintDebug(self):
    print ' Zp expr.'
    print 'expr: ', self.expr
    print 'expr.sum: ', self.expr.sum()
    print 'expr.sum.mod: ', (self.expr.sum() % PRIME)
    l = self.expr.shape[0]
    return str(self.expr[0:min(l, 2)]) + "..."

  @staticmethod
  def ConvertToOneElement(expr_mat, vals, shape_x, shape_y):
    ret = None
    for i in xrange(shape_x):
      for j in xrange(shape_y):
        v = expr_mat.expressions[min(i, expr_mat.shape[0] - 1), \
          min(j, expr_mat.shape[1] - 1)].expr * vals[i, j]
        if ret is None:
          ret = v % PRIME
        else:
          ret += v
          ret %= PRIME
    return ret

  @staticmethod
  def FindLinearCombination(expressions_list, target_expr):
    # Try to find linear combination of expressions from expressions_list
    # to express target_expr
    if len(expressions_list) == 0:
      return [], []
    ma = max(manage.config.N, manage.config.M)
    vals = np.random.random_integers(
        low=1, high=100, size=(ma, ma))

    st = target_expr.shape
    expressions_list_new = []
    for expr_mat in expressions_list:
      s = expr_mat.expressions.shape
      if (s[0] != st[0] and s[0] != 1) or \
         (s[1] != st[1] and s[1] != 1):
        continue
      expressions_list_new.append(expr_mat)

    expressions_list = expressions_list_new

    mat = []
    for i, expr_mat in enumerate(expressions_list):
      s = expr_mat.expressions.shape
      assert s[0] == st[0] or s[0] == 1
      assert s[1] == st[1] or s[1] == 1
      expression = \
        ExprZp.ConvertToOneElement(expr_mat, vals, st[0], st[1])
      # list of values
      mat.append(expression)

    # A shape: NUM_EVAL x num_expressions_of_size_1_1
    A = np.array(mat).transpose()

    b = ExprZp.ConvertToOneElement(target_expr, vals, st[0], st[1])

    x = solver.Solver().GaussP(A, b)
    weights = []
    comps = []
    for expr, elem in zip(expressions_list, x):
      if elem != 0:
        if elem >= PRIME / 2:
          elem = elem - PRIME
        weights.append(elem)
        comps.append(expr.comp)
    return weights, comps

  @classmethod
  def ToFrac(cls, number):
    frac_range = 2000
    sol = None
    score = 100000
    if abs(number) <= frac_range:
      return "%d" % number
    for i in range(-frac_range, frac_range):
      if i == 0:
        continue
      a = (number * i) % PRIME
      if abs(a) <= frac_range:
        g = gcd(a, i)
        new_score = abs(a / g) + abs(i / g)
        if new_score < score:
          sol = "%d / %d" % (a / g, i / g)
          score = new_score
    if sol is not None:
     return sol
    raise Exception("Not a frac")
  
  @classmethod
  def SolutionStr(cls, weights, comps):
    from manage.config import NUMPY, THEANO, MATLAB, THIS
    backs = [NUMPY, THEANO, MATLAB, THIS]
    names = ['NUMPY', 'THEANO', 'MATLAB', 'THIS']
    result_strs = {}
    for b, n in zip(backs, names):
      print "_" * 100
      print "Solution for %s:" % n
      result_strs[b] = ""
      for w, c in zip(weights, comps):
        if result_strs[b]:
          result_strs[b] += ' + \\\n'
        if w >= PRIME / 2:
          w = w - PRIME
        if w != 1:
          result_strs[b] += "%d * " % w
        result_strs[b] += c[b]
      print result_strs[b]
    return result_strs

