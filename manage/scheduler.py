#a!/usr/bin/python
import sys
import manage.config
from manage.rule import Rule
from manage.cache import Cache
import heapq
from manage.config import APPLIED_RULES

class Scheduler(object):

  def __init__(self, params):
    print "Creating Scheduler"
    self.params = params
    self.Reset()
    assert manage.config.N != manage.config.M

  def Reset(self):
    self.old_score = -1
    self.old_rules_dict_size = -1
    self.old_rules_dict_small_size = -1
    self.score = 0
    self.cache = Cache()
    self.solution = None
    self.cache_size = -1
    self.rules = []
    self.pq = []  # Priority queue

  def Train(self, data):
    pass

  def SetTarget(self, target):
    self.target = target
    self.AddO2Rules()
    self.AddO2MultRules()
    if target.complexity == 3:
      self.AddO3Rules()
    start_expressions = target.GetStartSymbols()
    for start_expression in start_expressions:
      self.cache.Add(start_expression)
      self.AddNonTried(start_expression)

  def _Add(self, name, arg1shape, arg2shape=None, params=None):
    rule = Rule(name, params)
    shapes = []
    if rule not in self.rules:
      self.rules.append(rule)
    idx = self.rules.index(rule)
    self.rules[idx].idx = idx
    shapes = self.rules[idx].shapes
    shapes.append((arg1shape, arg2shape))
    self.rules[idx].shapes = shapes

  def AddO2Rules(self):
    print 'Registering O(n^2) general rules'
    n = manage.config.N
    m = manage.config.M
    self._Add('Marginalize', (n, m), None, {'axis': 0})
    self._Add('Marginalize', (n, m), None, {'axis': 1})
    self._Add('Marginalize', (n, 1), None, {'axis': 0})
    self._Add('Marginalize', (1, m), None, {'axis': 1})
    self._Add('Marginalize', (m, n), None, {'axis': 0})
    self._Add('Marginalize', (m, m), None, {'axis': 0})
    self._Add('Marginalize', (n, n), None, {'axis': 0})
    self._Add('Marginalize', (m, n), None, {'axis': 1})
    self._Add('Marginalize', (m, m), None, {'axis': 1})
    self._Add('Marginalize', (n, n), None, {'axis': 1})
    self._Add('Marginalize', (1, n), None, {'axis': 1})
    self._Add('Marginalize', (m, 1), None, {'axis': 0})

    for i in (n, m, 1):
      for j in (n, m, 1):
        if i != 1 or j != 1:
          self._Add('Transpose', (i, j), None, None)

    for i in (n, m, 1):
      for j in (n, m, 1):
        for k in (n, m, 1):
          for l in (n, m, 1):
            if (i, j) == (k, l) or (i == k and j == 1) or \
              (i == k and l == 1) or (j == l and i == 1) or \
              (j == l and k == 1) or (i == 1 and j == 1) or \
              (k == 1 and l == 1):
              self._Add('ElementwiseMultiply', (i, j), (k, l), None)

  def AddO2MultRules(self):
    print 'Registering O(n^2) mult rules'
    sizes = (manage.config.N, manage.config.M, 1)
    for i in sizes:
      for j in sizes:
        for k in sizes:
          if i == 1 or j == 1 or k == 1:
            self._Add('Multiply', (i, j), (j, k), None)

  def AddO3Rules(self):
    print 'Registering O(n^3) rules'
    sizes = (manage.config.N, manage.config.M)
    for i in sizes:
      for j in sizes:
        for k in sizes:
          self._Add('Multiply', (i, j), (j, k), None)

  def AddNonTried(self, new_expr):
    to_push = set()
    for rule in self.rules:
      for shape in rule.shapes:
        if shape[0] == new_expr.shape or shape[1] == new_expr.shape:
          if shape[1] is None:
            if not self.cache.Pushed(rule, new_expr, None):
              to_push.add((rule, new_expr, None))
          else:
            if shape[0] == new_expr.shape:
              for _, expr2 in self.cache.GetExpressions(shape[1]).iteritems():
                if not self.cache.Pushed(rule, new_expr, expr2):
                  to_push.add((rule, new_expr, expr2))
            else:
              for _, expr1 in self.cache.GetExpressions(shape[0]).iteritems():
                if not self.cache.Pushed(rule, expr1, new_expr):
                  to_push.add((rule, expr1, new_expr))

    for rule, expr1, expr2 in to_push:
      self.cache.SetPushed(rule, expr1, expr2)
      c = self.GetEval(rule, expr1, expr2)
      heapq.heappush(self.pq, (c, (rule, expr1, expr2)))

  def Apply(self, rule, matrix, other_matrix):
    if self.score % 100 == 0:
      sys.stdout.write('.')
      sys.stdout.flush()
    self.score += 1
    if other_matrix is None:
      new_expr = rule.ApplyOneArg(matrix)
      self.cache.SetTried(rule.idx, matrix)
    else:
      new_expr = rule.ApplyTwoArg(matrix, other_matrix)
      self.cache.SetTried(rule.idx, matrix, other_matrix)
    self.cache.Add(new_expr)

    if new_expr is not None:
      self.AddNonTried(new_expr)
    return new_expr

  def FoundTarget(self):
    if self.target is None or self.target.GetTargetExpression() is None:
      return False
    power = self.target.GetTargetExpression().powers[0]
    if self.old_score == self.score:
      print "DEADLOCK"
      exit(-1)
    else:
      self.old_score = self.score
    rules_dict = self.cache.GetExpressions((1, 1)).values()
    if len(rules_dict) == self.old_rules_dict_size:
      return False
    self.old_rules_dict_size = len(rules_dict)
    rules_dict_small = []
    for r in rules_dict:
      if r.shape == (1, 1) and r.powers[0] == power:
        rules_dict_small.append(r)
    if len(rules_dict_small) == self.old_rules_dict_small_size:
      return False
    self.old_rules_dict_small_size = len(rules_dict_small)
    if manage.config.NUM_EVAL < len(rules_dict_small) or \
       manage.config.NUM_EVAL > len(rules_dict_small) * 2:
      manage.config.NUM_EVAL = \
        max(int(len(rules_dict_small) * 1.05), manage.config.NUM_HASH) + 10
      self.target.Compute()
      A = self.target.GetStartSymbols()[0]
      if len(self.target.GetStartSymbols()) > 1:
        B = self.target.GetStartSymbols()[1]
      rules_dict_long_eval = []
      for r in rules_dict_small:
        rules_dict_long_eval.append(eval(r.comp[manage.config.THIS]))
    else:
      rules_dict_long_eval = rules_dict_small

    self.solution = manage.config.EXPR_IMPL.FindLinearCombination(
      rules_dict_long_eval, self.target.GetTargetExpression())
    weights, comps = self.solution
    if len(weights) == 0:
      return False
    return True

  def GetExpressions(self):
    exprs = []
    for i in (1, manage.config.N, manage.config.M):
      for j in (1, manage.config.N, manage.config.M):
        exprs += self.cache.GetExpressions((i, j)).values()
    return exprs

  def GetExpressionsPerRule(self, rule):
    return self.cache.non_tried[rule.idx]

  def Run(self):
    while len(self.pq) > 0:
      score, best_elem = heapq.heappop(self.pq)
      rule, expr1, expr2 = best_elem
      self.Apply(rule, expr1, expr2)
      if self.FoundTarget():
        return
    raise TargetNotFound("No new expression before FoundTarget")

class TargetNotFound(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)
