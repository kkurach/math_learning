import numpy as np
from manage.config import MAX_NUM_VARIABLES, MAX_POWER, PRIME

RAND_VALS = None

def GetRandVals():
  global RAND_VALS
  if RAND_VALS is not None:
    return RAND_VALS
  np.random.seed(123)
  evals = 2000
  RAND_VALS = np.random.random_integers(
    low=1,
    high=PRIME - 1,
    size=(evals, MAX_NUM_VARIABLES, MAX_POWER))
  RAND_VALS = RAND_VALS.astype(np.int64)
  for i in xrange(evals):
    for j in xrange(MAX_NUM_VARIABLES):
      RAND_VALS[i][j][0] = long(1)

  tolong = np.vectorize(long)
  RAND_VALS = tolong(RAND_VALS)
  for k in xrange(2, MAX_POWER):
    RAND_VALS[:, :, k] = (
        (RAND_VALS[:, :, k-1] * RAND_VALS[:, :, 1]) % PRIME)
  RAND_VALS = RAND_VALS.astype(np.int64)
  return RAND_VALS

def MyPow(a, n, m):
  a = long(a)
  n = long(n)
  m = long(m)
  ret = long(1)
  while n > 0:
    if n % 2 == 1:
      ret = (ret * a) % m
    a = (a * a) % m
    n /= 2
  return ret

def RevMod(a, p):
  if type(a) is np.array or type(a) is np.ndarray:
    def rev_mod_fun(e):
      return RevMod(e, p)
    rev_mod_fun = np.vectorize(rev_mod_fun)
    return rev_mod_fun(a).astype(np.int64)
  if a == 1:
    return long(1)
  return MyPow(long(a) % long(p), long(p-2), long(p))

