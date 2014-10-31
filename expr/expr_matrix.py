import numpy as np
import manage.config
from manage.config import NUMPY, THEANO, MATLAB, THIS, MAXPOWER, APPLIED_RULES, READABLE_RULES
import expr.expr_common as expr_common
import copy
import hashlib

class ExprMatrix(object):

  # expressions is of type np.array
  def __init__(self, comp, expressions, powers, ops=1):
    if type(powers) is list:
      powers = np.array(powers)
    if type(comp) is str:
      self.comp = {NUMPY: comp, THEANO: comp, MATLAB: comp, THIS: comp, APPLIED_RULES: comp, READABLE_RULES: comp}
      if len(comp) == 1:
        self.comp[APPLIED_RULES] = None
        self.comp[READABLE_RULES] = None
    else:
      self.comp = comp # It is a dictionary.
    assert expressions is not None
    assert type(expressions) == np.ndarray
    assert expressions.ndim == 2

    self.expressions = expressions
    self.hashval = None
    self.powers = powers
    assert self.powers.shape[0] == manage.config.MAXPOWER.shape[0]
    self.ops = ops
    self.sha = None
    self.tnn_vec = None

  def HashSha(self):
    if self.sha is None:
      self.sha = hashlib.sha1(self.Hash()).hexdigest()
    return self.sha

  def Hash(self):
    self._UpdateHash()
    return self.hashval

  def __eq__(self, obj_expr_symbolic):
    def norm(A):
      return np.sum(np.abs(A))
    eq = norm(self.Hash() - obj_expr_symbolic.Hash()) == 0
    return eq

  @property
  def shape(self):
    return self.expressions.shape

  def _UpdateHash(self):
    if self.hashval is not None:
      return
    vec = []
    n, m, P = manage.config.N, manage.config.M, manage.config.PRIME
    nm = max([n, m, self.expressions.shape[0], self.expressions.shape[1]])
    vec = np.zeros((manage.config.NUM_HASH, nm * nm))
    for i in xrange(self.expressions.shape[0]):
      for j in xrange(self.expressions.shape[1]):
        vec[:, i * nm + j] = np.mod(self.expressions[i, j].Hash(), P)
    s = np.sum(vec) % P
    inverse_mod = expr_common.RevMod(s, P)
    vec = np.mod(vec * inverse_mod, P)
    mult = np.multiply(vec, expr_common.RAND_VALS[0, 0:(nm*nm), 2])
    self.hashval = np.mod(np.sum(np.mod(mult, P), axis=1), P)

  def ElementwiseMultiply(self, other):
    if isinstance(other, (int, long, float, np.int64)):
      expressions = np.multiply(self.expressions, other)
      comp = {k: "(%s * %s)" % \
        (str(other), str(v)) for k, v in self.comp.items()}
      comp[THIS] = "(%s).ElementwiseMultiply(%s)" % \
        (self.comp[THIS], str(other))
      return ExprMatrix(comp, expressions, self.powers, self.ops)
    powers = self.powers + other.powers
    if (powers > manage.config.MAXPOWER).any():
      return None
    expressions = self.expressions * other.expressions
    comp = {NUMPY: '(%s * %s)' % (self.comp[NUMPY], other.comp[NUMPY]),
            THEANO: '(%s * %s)' % (self.comp[THEANO], other.comp[THEANO]),
            MATLAB: '(%s .* %s)' % (self.comp[MATLAB], other.comp[MATLAB]),
            THIS: '(%s).ElementwiseMultiply(%s)' % \
              (self.comp[THIS], other.comp[THIS]),
            APPLIED_RULES: (3, self.comp[APPLIED_RULES], other.comp[APPLIED_RULES]),
            READABLE_RULES: ('.*', self.comp[READABLE_RULES], other.comp[READABLE_RULES])}
    ops = self.ops + other.ops + 1
    return ExprMatrix(comp, expressions, powers, ops)

  def Power(self, k):
    powers = self.powers * k
    if (powers > manage.config.MAXPOWER).any():
      return None
    expressions = np.power(self.expressions, k)
    comp = {NUMPY: '(np.power(%s, %d))' % (self.comp[NUMPY], k),
            THEANO: '(%s ** %d)' % (self.comp[THEANO], k),
            MATLAB: '(%s .^ %d)' % (self.comp[MATLAB], k),
            THIS: '(%s).Power(%s)' % (self.comp[THIS], str(k)),
            APPLIED_RULES: (float('Inf'), self.comp[APPLIED_RULES]),
            READABLE_RULES: (float('Inf'), self.comp[READABLE_RULES])}
    return ExprMatrix(comp, expressions, powers, self.ops + 1)

  def Add(self, other):
    if isinstance(other, (int, long, float, np.int64)):
      expressions = self.expressions + other
      comp = {k: "(%s + %s)" % \
        (str(v), str(other)) for k, v in self.comp.items()}
      comp[THIS] = "(%s).Add(%s)" % (self.comp[THIS], str(other))
      return ExprMatrix(comp, expressions, self.powers, self.ops)
    expressions = self.expressions + other.expressions
    items = self.comp.items()
    comp = {k: "(%s + %s)" % (str(v), str(other.comp[k])) for k, v in items}
    comp[THIS] = "(%s).Add(%s)" % (self.comp[THIS], other.comp[THIS])
    comp[APPLIED_RULES] = (float('Inf'), self.comp[APPLIED_RULES], other.comp[APPLIED_RULES])
    comp[READABLE_RULES] = (float('Inf'), self.comp[READABLE_RULES], other.comp[READABLE_RULES])
    powers = np.maximum(self.powers, other.powers)
    ops = self.ops + other.ops + 1
    return ExprMatrix(comp, expressions, powers, ops)

  def Sub(self, other):
    if isinstance(other, (int, long, float, np.int64)):
      expressions = self.expressions - other
      comp = {k: "(%s - %s)" % \
        (str(v), str(other)) for k, v in self.comp.items()}
      comp[THIS] = "(%s).Sub(%s)" % (self.comp[THIS], str(other))
      return ExprMatrix(comp, expressions, self.powers, self.ops)
    expressions = self.expressions - other.expressions
    items = self.comp.items()
    comp = {k: "(%s - %s)" % (str(v), str(other.comp[k])) for k, v in items}
    comp[THIS] = "(%s).Sub(%s)" % (self.comp[THIS], other.comp[THIS])
    comp[APPLIED_RULES] = (float('Inf'), self.comp[APPLIED_RULES], other.comp[APPLIED_RULES])
    comp[READABLE_RULES] = (float('Inf'), self.comp[READABLE_RULES], other.comp[READABLE_RULES])
    powers = np.maximum(self.powers, other.powers)
    ops = self.ops + other.ops + 1
    return ExprMatrix(comp, expressions, powers, ops)

  def Multiply(self, other):
    if isinstance(other, (int, long, float, np.int64)):
      expressions = self.expressions * other
      comp = {k: "(%s * %s)" % \
        (str(v), str(other)) for k, v in self.comp.items()}
      comp[THIS] = "(%s).Multiply(%s)" % (self.comp[THIS], str(other))
      return ExprMatrix(comp, expressions, self.powers, self.ops)
    powers = self.powers + other.powers
    if (powers > manage.config.MAXPOWER).any():
      return None
    expressions = np.dot(self.expressions, other.expressions)
    comp = {NUMPY: '(np.dot(%s, %s))' % (self.comp[NUMPY], other.comp[NUMPY]),
            THEANO: 'T.dot(%s, %s)' % (self.comp[THEANO], other.comp[THEANO]),
            MATLAB: '(%s * %s)' % (self.comp[MATLAB], other.comp[MATLAB]),
            THIS: '(%s).Multiply(%s)' % (self.comp[THIS], other.comp[THIS]),
            APPLIED_RULES: (4, self.comp[APPLIED_RULES], other.comp[APPLIED_RULES]),
            READABLE_RULES: ('*', self.comp[READABLE_RULES], other.comp[READABLE_RULES])}
    ops = self.ops + other.ops + 1
    return ExprMatrix(comp, expressions, powers, ops)

  def Transpose(self):
    expressions = self.expressions.transpose()
    comp = {NUMPY: '(%s.transpose())' % self.comp[NUMPY],
            THEANO: '(%s.T)'% self.comp[THEANO],
            MATLAB: '(%s\')'% self.comp[MATLAB],
            THIS: '(%s).Transpose()'% self.comp[THIS],
            APPLIED_RULES: (2, self.comp[APPLIED_RULES]),
            READABLE_RULES: ('^T', self.comp[READABLE_RULES])}
    return ExprMatrix(comp, expressions, self.powers, self.ops + 1)

  def Marginalize(self, axis):
    if axis is None:
      return self.Marginalize(0).Marginalize(1)
    expressions = np.sum(self.expressions, axis=axis, keepdims=True)
    if type(expressions) != np.array:
      # Make 1x1 elemen matrix
      expressions = np.array(expressions)
    idx = 0 + axis
    comp = {
        NUMPY: '(np.sum(%s, axis=%s, keepdims=True))' % (
          self.comp[NUMPY], axis),
        THEANO: '(T.sum(%s, axis=%s, keepdims=True))' % (
          self.comp[THEANO], axis),
        MATLAB: '(sum(%s, %s))' % (self.comp[MATLAB], axis + 1),
        THIS: '(%s).Marginalize(%s)' % (self.comp[THIS], axis),
        APPLIED_RULES: (idx, self.comp[APPLIED_RULES]),
        READABLE_RULES: ('\sum_%d' % idx, self.comp[READABLE_RULES])}
    return ExprMatrix(comp, expressions, self.powers, self.ops + 1)

  def __str__(self):
    s = 'Hash: %s,' % str(self.Hash())
    s += 'Comp: %s,' % str(self.comp)
    s += "Size: %d x %d," % (
        self.expressions.shape[0], self.expressions.shape[1])
    for i in xrange(self.expressions.shape[0]):
      for j in xrange(self.expressions.shape[1]):
        s += '[' +  self.expressions[i, j].DebugString() + ']'
    return s

  def PrintDebug(self):
    print self.__str__()

  def __mul__(self, other):
    return self.Multiply(other)

  def __rmul__(self, other):
    return self.Multiply(other)

  def __add__(self, other):
    return self.Add(other)

  def __radd__(self, other):
    return self.Add(other)

