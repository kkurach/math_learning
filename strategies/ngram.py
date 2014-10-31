from manage.scheduler import Scheduler
import numpy as np
import operator
from expr.expr_matrix import ExprMatrix
from collections import defaultdict
import hashlib
from manage.config import APPLIED_RULES

class NgramScheduler(Scheduler):

  def __init__(self, params):
    Scheduler.__init__(self, params)
    self.counts = [defaultdict(int)] * (self.params['depth'] + 1)

  def __str__(self):
    return "NgramScheduler%d" % self.params['depth']

  def add(self, dict1, dict2):
    for k, v in dict2.iteritems():
      dict1[k] += v
    return dict1

  def ngram(self, data, depth, s):
    counts = defaultdict(int)
    if type(data) is list:
      for d in data:
        counts = self.add(counts, self.ngram(d, depth, s))
    elif data is not None:
      if len(data) == 2:
        _, expr1 = data
        counts = self.ngram(expr1, depth, s)
      else:
        _, expr1, expr2 = data
        counts1 = self.ngram(expr1, depth, s)
        counts2 = self.ngram(expr2, depth, s)
        counts = self.add(counts1, counts2)
      counts[fasthash(self.deep_node_name(data, depth))] += 1
    return counts
  
  def Train(self, data):
    if data is None:
      return
    s = len(self.rules) + 1
    depth = self.params['depth']
    for d in range(1, depth + 1):
      counts = self.ngram(data, d, s)
      self.counts[d] = self.add(self.counts[d], counts)

  def deep_node_name(self, node, depth):
    if type(node) is ExprMatrix:
      return self.deep_node_name(node.comp[APPLIED_RULES], depth)
    if node is None:
      return [-1] * ((2 ** depth) - 1)
    if depth == 0:
      return []
    if depth == 1:
      return [node[0]]
    else:
      node2 = None
      if len(node) == 3:
        node2 = node[2]
      return [node[0]] + self.deep_node_name(node[1], depth - 1) \
                       + self.deep_node_name(node2, depth - 1)

  def GetEval(self, rule, expr1, expr2):
    if len(self.counts) == 0:
      return 0
    for d in range(self.params['depth'], 0, -1):
      a = self.deep_node_name(expr1, d - 1)
      b = self.deep_node_name(expr2, d - 1)
      idx = [rule.idx] + a + b
      c = -self.counts[d][fasthash(idx)]
      if c != 0:
        return c * (10 ** d)
    return 0


def fasthash(a):
  return hashlib.sha1(np.array(a)).hexdigest()

