class Rule(object):

  def __init__(self, name, params=None):
    self.name = name
    self.params = params
    self.shapes = []

  def idx(self):
    idxs = {'Transpose': 2, 'ElementwiseMultiply': 3, 'Multiply': 4}
    if self.name == 'Marginalize':
      return 0 + self.params['axis']
    else:
      return idxs[self.name]

  def ApplyOneArg(self, matrix):
    if self.name == 'Transpose':
      ret = matrix.Transpose()
    elif self.name == 'Exp':
      ret = matrix.Exp(power=self.params['power'])
    elif self.name == 'Marginalize':
      ret = matrix.Marginalize(axis=self.params['axis'])
    else:
      raise Exception('Unknown one arg operation: %s' % self.name)
    return ret

  def ApplyTwoArg(self, matrix, other_matrix):
    if self.name == 'ElementwiseMultiply':
      ret = matrix.ElementwiseMultiply(other_matrix)

    elif self.name == 'Multiply':
      ret = matrix.Multiply(other_matrix)
    else:
      raise Exception('Unknown two arg operation: %s' % self.name)
    return ret

  def __str__(self):
    return 'Rule %s, params: %s' % (self.name, self.params)

  def Hash(self):
    return str(self)

  def __eq__(self, other):
    return self.Hash() == other.Hash()

