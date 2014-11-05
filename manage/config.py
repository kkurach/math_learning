import numpy as np

NUMPY = 1
THEANO = 2
MATLAB = 3
THIS = 4
APPLIED_RULES = 5
READABLE_RULES = 6

N = 2
M = 3
MAXPOWER = np.array([1, 2, 3])
EXPR_IMPL = None

PRIME = long(9000223)
PRIME2 = long(1009)
NUM_HASH = 20

# const values for Zp implementation
NUM_EVAL = 1000
MAX_NUM_VARIABLES = 400
MAX_POWER = 20

def get():
  return {'N': N, 'M': M, 'MAXPOWER': MAXPOWER, 'EXPR_IMPL': EXPR_IMPL}

def upload(opt):
  global N, M, MAXPOWER, EXPR_IMPL
  N = opt.get('N')
  M = opt.get('M')
  MAXPOWER = opt.get('MAXPOWER')
  EXPR_IMPL = opt.get('EXPR_IMPL')
