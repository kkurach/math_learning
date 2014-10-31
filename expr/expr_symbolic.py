from manage.config import PRIME, NUM_HASH
import manage.config
import hashlib
import copy
import expr.expr_abstract as expr_abstract
import expr.expr_common as expr_common
import numpy as np
from manage import solver
from math import factorial
from fractions import Fraction as F

class ExprSymbolic(expr_abstract.ExprAbstract):

  # expr vectors should be a list of vectors representing variables
  def __init__(self, quants, expr_vectors=None):
    if type(quants) is list:  # FIXME(karol): quants should be always array
      if type(quants[0]) is not F:
        quants = map(F, quants)
      quants = np.array(quants)
    self.hashval = None
    assert type(expr_vectors) == np.ndarray
    assert expr_vectors.ndim == 2
    assert expr_vectors.shape[0] == len(quants)

    expr_vectors = expr_vectors.astype(np.int64)
    if all(q == 0 for q in quants):
      quants = np.array([F(0)])
      expr_vectors = np.array([expr_vectors[0]])
    super(ExprSymbolic, self).__init__(quants, expr_vectors)
    self.quants = quants
    self.expr_vectors = expr_vectors
    assert self.expr_vectors.ndim == 2

  def Hash(self):
    if self.hashval is not None:
      return self.hashval
    rand_vals = expr_common.GetRandVals()
    P = PRIME
    if (self.quants is None) or \
         (len(self.quants) == 1 and self.quants[0] == 0):
      return 0
    a = np.ones(shape=(NUM_HASH, self.expr_vectors.shape[0]), \
      dtype=np.int64)
    for j in xrange(self.expr_vectors.shape[1]):
      a = np.multiply(a, \
        rand_vals[xrange(NUM_HASH)][:, j, self.expr_vectors[:, j]]) % P
    numerators = np.vectorize(lambda x: x.numerator)(self.quants)
    denoms = np.vectorize(lambda x: x.denominator)(self.quants)
    inv = expr_common.RevMod(denoms, P)
    inv = inv.astype(np.int64)
    q = np.multiply(numerators, inv)
    h = np.array(np.mod(np.sum(np.mod(a * q, P), axis=1), P))
    self.hashval = h
    return h

  @staticmethod
  def _ExprSymbolicFromHashmap(hash2quant, hash2expr):
    quants = []
    expr_vectors = []
    zero = None
    for hash_val, expr_vector in hash2expr.iteritems():
      q = hash2quant[hash_val]
      if q == 0:
        assert expr_vector.ndim == 1
        zero = np.array([np.zeros(len(expr_vector))])
        continue
      expr_vectors.append(expr_vector)
      quants.append(q)
    if len(quants) == 0:
      return ExprSymbolic([F(0)], zero)
    else:
      return ExprSymbolic(quants, np.array(expr_vectors))

  def __mul__(self, other):
    if isinstance(other, (int, long, float, np.int64, F)):
      return ExprSymbolic(self.quants * other, self.expr_vectors)
    else:
      hash2e = {}
      hash2q = {}
      for q, e in zip(self.quants, self.expr_vectors):
        for o_q, o_e in zip(other.quants, other.expr_vectors):
          assert len(e) == len(o_e)
          new_e = e + o_e
          h = hashlib.sha1(new_e).hexdigest()
          hash2e[h] = new_e
          hash2q[h] = hash2q.get(h, F(0)) + q * o_q
      expr = self._ExprSymbolicFromHashmap(hash2q, hash2e)
      if self.hashval is not None and other.hashval is not None:
        expr.hashval = np.mod(self.Hash() * other.Hash(), PRIME)
      return expr

  def __sub__(self, other):
    if isinstance(other, (int, long, float, np.int64)):
      other = -other
    else:
      q = copy.copy(other.quants)
      q = q * -1
      other = ExprSymbolic(q, other.expr_vectors)
    return self.__add__(other)

  def __add__(self, other):
    if isinstance(other, (int, long, float, np.int64)):
      e = np.zeros((1, self.expr_vectors.shape[1]), dtype=np.int64)
      return self.__add__(ExprSymbolic([F(other)], e))
    hash2q = {}
    hash2e = {}
    quants = np.concatenate((self.quants, other.quants))
    expr_vectors = np.vstack((self.expr_vectors, other.expr_vectors))
    for q, e in zip(quants, expr_vectors):
      h = hashlib.sha1(e).hexdigest()
      hash2e[h] = e
      hash2q[h] = hash2q.get(h, F(0)) + q
    expr = self._ExprSymbolicFromHashmap(hash2q, hash2e)
    if self.hashval is not None and other.hashval is not None:
      expr.hashval = np.mod(self.Hash() + other.Hash(), PRIME)
    return expr

  def __eq__(self, obj_expr_symbolic):
    return (self.Hash() == obj_expr_symbolic.Hash()).all()

  def DebugString(self):
    ret = []
    if len(self.quants) == 0:
      ret = ['0']
    zipped = zip(self.quants, self.expr_vectors)
    for k, (quant, expr_vector) in enumerate(zipped):
      assert expr_vector.ndim == 1
      if k > 0:
        ret.append(" + ")
      if quant != 1 or (expr_vector == 0).all():
        ret.append("%s" % str(quant))
      if (expr_vector == 0).all():
        continue
      for i in xrange(expr_vector.shape[0]):
        if expr_vector[i] != 0:
          ret += [chr(ord('a') + i % 26)] * int(1 + i / 26)
          if expr_vector[i] > 1:
            ret.append("^%d" % expr_vector[i])
    return ''.join(ret)

  def __str__(self):
    s = 'Expr (len = %d) ' % len(self.quants)
    for q, e in zip(self.quants, self.expr_vectors):
      n = q.numerator
      d = q.denominator
      s += 'quant: %d / %d expr_vector: %s, ' % (n, d, e)
    return s

  def PrintDebug(self):
    print self.__str__()

  @staticmethod
  def FindLinearCombination(rules_list, target_expr):
    print "Target expr: ", target_expr
    print "Rules: "
    for r in rules_list:
      print r
    # Try to find linear combination of rules from rules_list
    # to express target_expr
    num_unique_hashes = 0
    expr2index = {}
    target_expr_set = set()
    rules_expr_set = set()
    st = target_expr.shape

    rules_list_new = []
    for rule in rules_list:
      s = rule.expressions.shape
      if (s[0] != st[0] and s[0] != 1) or (s[1] != st[1] and s[1] != 1):
        continue
      rules_list_new.append(rule)
    rules_list = rules_list_new

    for i, rule in enumerate(rules_list):
      s = rule.expressions.shape
      assert s[0] == st[0] or s[0] == 1
      assert s[1] == st[1] or s[1] == 1
      for x in xrange(rule.expressions.shape[0]):
        for y in xrange(rule.expressions.shape[1]):
          for expr_vector in rule.expressions[x, y].expr_vectors:
            h = hashlib.sha1(expr_vector).hexdigest()
            rules_expr_set.add(h)
            if h not in expr2index:
              expr2index[h] = num_unique_hashes
              num_unique_hashes += 1

    for x in xrange(st[0]):
      for y in xrange(st[1]):
        for expr_vector in target_expr.expressions[x, y].expr_vectors:
          h = hashlib.sha1(expr_vector).hexdigest()
          target_expr_set.add(h)
          if h not in expr2index:
            expr2index[h] = num_unique_hashes
            num_unique_hashes += 1

    for expr in target_expr_set:
      if expr not in rules_expr_set:
        print 'Checking expr: ', expr
      assert expr in rules_expr_set

    # create matrix num_unique_hashes x len(rules)
    s = num_unique_hashes * target_expr.shape[0] * target_expr.shape[1]
    print 'Creating matrix %d x %d' % (s, len(rules_list))
    A = []
    for i, rule in enumerate(rules_list):
      s = rule.expressions.shape
      if (s[0] != st[0] and s[0] != 1) or (s[1] != st[1] and s[1] != 1):
        continue
      a = ExprSymbolic._ConvertExpressionsToVector(
          rule.expressions, expr2index, st[0], st[1])
      A.append(a)
    A = np.array(A).transpose()
    b = ExprSymbolic._ConvertExpressionsToVector(
        target_expr.expressions, expr2index, st[0], st[1])
    b = np.array(b).transpose()
    x = solver.Solver.GaussF(A, b)

    if len(x) == 0:
      print "COULD NOT FIND SOLUTION"
      return
    assert len(x) == len(rules_list)
    weights = []
    comps = []
    for i, t in zip(xrange(len(x)), x):
      if t != 0:
        weights.append(t)
        comps.append(rules_list[i].comp)
    return weights, comps

  @classmethod
  def SolutionStr(cls, weights, comps):
    from manage.config import NUMPY, THEANO, MATLAB, THIS
    backs = [NUMPY, THEANO, MATLAB, THIS]
    result_strs = {}
    for b in backs:
      result_strs[b] = ""
      for w, c in zip(weights, comps):
        if result_strs[b]:
          result_strs[b] += " + \\\n"
        if w.denominator == 1:
          if w.numerator != 1:
            result_strs[b] += "%d. *" % w.numerator
        else:
          result_strs[b] += "(%d. / %d.)*" % (w.numerator, w.denominator)
        result_strs[b] += "%s" % c[b]
    return result_strs

  @staticmethod
  def _ConvertExpressionsToVector(expr, expr2index, shape_x, shape_y):
    n = max(expr2index.values()) + 1
    vec = [F(0)] * n * shape_x * shape_y
    assert expr.shape[0] == shape_x or expr.shape[0] == 1
    assert expr.shape[1] == shape_y or expr.shape[1] == 1
    for x in xrange(expr.shape[0]):
      for y in xrange(expr.shape[1]):
        assert len(expr[x, y].expr_vectors) == len(expr[x, y].quants)
        for q, e in zip(expr[x, y].quants, expr[x, y].expr_vectors):
          h = hashlib.sha1(e).hexdigest()
          assert h in expr2index
          for xx in xrange(shape_x / expr.shape[0]):
            for yy in xrange(shape_y / expr.shape[1]):
              vec[expr2index[h] + ((x + xx) * shape_y + (y + yy)) * n] = q
    return vec
