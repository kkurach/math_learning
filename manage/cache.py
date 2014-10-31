import copy

class Cache(object):

  def __init__(self):
    # map (n, m) -> dict
    self.grammars = {}
    self.tried = set()
    self.pushed = set()
    self.non_tried = {} # map rule hash -> set()

  def GetSize(self):
    ret = 0
    for _, d in self.grammars.iteritems():
      ret += len(d)
    return ret

  def GetExpressions(self, size_tuple):
    if size_tuple not in self.grammars:
      self.grammars[size_tuple] = {}
    return self.grammars[size_tuple]

  def Add(self, expr_matrix):
    if expr_matrix is None:
      return False
    size_tuple = expr_matrix.expressions.shape
    if size_tuple not in self.grammars:
      self.grammars[size_tuple] = {}

    h = expr_matrix.HashSha()
    should_add = ((h not in self.grammars[size_tuple]) or
                  (self.grammars[size_tuple][h].ops > expr_matrix.ops))
    if should_add:
      self.grammars[size_tuple][h] = expr_matrix
      return True
    return False
  
  def ArrayGet(self, array, rule, expr1, expr2):
    rule_idx = rule.idx
    hash1 = expr1.HashSha()
    hash2 = None
    if expr2 is not None:
      hash2 = expr2.HashSha()
    return (rule_idx, hash1, hash2) in array
  
  def ArraySet(self, array, rule_idx, expr1, expr2):
    hash1 = expr1.HashSha()
    hash2 = None
    if expr2 is not None:
      hash2 = expr2.HashSha()
    array.add((rule_idx, hash1, hash2))

  def Tried(self, rule, expr1, expr2=None):
    return self.ArrayGet(self.tried, rule, expr1, expr2)

  def SetTried(self, rule_idx, expr1, expr2=None):
    self.ArraySet(self.tried, rule_idx, expr1, expr2)

  def Pushed(self, rule, expr1, expr2=None):
    return self.ArrayGet(self.pushed, rule, expr1, expr2)

  def SetPushed(self, rule, expr1, expr2=None):
    self.ArraySet(self.pushed, rule.idx, expr1, expr2)
