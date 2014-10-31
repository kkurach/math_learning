import copy
from manage.cache import Cache
import os
from manage.config import MATLAB

class MockCache(Cache):

  def __init__(self):
    Cache.__init__(self)

  def Add(self, expr_matrix):
    if expr_matrix is None:
      return False
    size_tuple = expr_matrix.expressions.shape
    if size_tuple not in self.grammars:
      self.grammars[size_tuple] = {}

    h = expr_matrix.HashSha()
    should_add = ((h not in self.grammars[size_tuple]) or
                  (self.grammars[size_tuple][h].ops > expr_matrix.ops))
    fname = "training/matlab/" + h + ".txt"
    data = []
    if os.path.isfile(fname):
      with open(fname) as f:
        data = f.readlines()
    data.append(str(expr_matrix.comp[MATLAB]) + "\n")
    data = set(data)

    with open(fname, 'w') as f:
      for d in data:
        f.write(d)
    if should_add:
      self.grammars[size_tuple][h] = expr_matrix
      return True
    return False
