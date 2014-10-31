#!/usr/bin/python
import manage.config
import sys
import math
import numpy as np
import os
import os.path
import signal
import unittest
import decimal
from decimal import Decimal, getcontext
from rbm_main import MainTrainRBM
from manage.config import NUMPY, THIS
from expr.expr_symbolic import ExprSymbolic
from expr.expr_zp import ExprZp
from manage.scheduler import Scheduler
from targets.rbm import RBM
from targets.rbm import Z
from targets.sum_AB import SumAB
from targets.target import Target
trained = {}

class End2EndTests(object):

  def __init__(self, impl):
    getcontext().prec = 100
    self.impl = impl
    manage.config.EXPR_IMPL = self.impl
    self.rules_dict = None

  def train(self, p, n, m):
    manage.config.EXPR_IMPL = self.impl
    manage.config.N = n
    manage.config.M = m
    r = "rules_" + self.impl.__name__ + str(p) + "_" + str(n) + "_" + str(m)
    if r not in trained:
      signal.signal(signal.SIGALRM, handler)
      signal.alarm(1000)
      if os.path.isfile(r):
        os.remove(r)
      manage.config.MAXPOWER = np.array(p)
      try:
        sched = Scheduler()
        target_expr = Target()
        target_expr.SetStartSymbols(len(p))
        sched.SetStartExpressions(target_expr.GetStartSymbols())
        sched.AddO2Rules()
        sched.AddO2MultRules()
        sched.Run()
        sol = []
        for i in (manage.config.N, manage.config.M, 1):
          for j in (manage.config.N, manage.config.M, 1):
            sol += sched.cache.GetExpressions((i, j)).values()
        trained[r] = sol
      except OSError, exc:
        print "Exception", exc
        self.assertTrue(False)
    return trained[r]

  # Verifies that size of grammar for Zp and symbolic is equal.
  def tearDown(self):
    for k0, c0 in trained.items():
      k1 = k0.replace('ExprZp', 'ExprSymbolic')
      if k1 in trained:
        c1 = trained[k1]
        if len(c0) != len(c1):
          for e0 in c0:
            print e0.comp[NUMPY]
          print
          for e1 in c1:
            print e1.comp[NUMPY]
        for e0 in c1:
          self.assertTrue(e0 in c1)
        for e1 in c0:
          self.assertTrue(e1 in c0)

  def testSumAB(self):
    print "Running testSum_AB test for %s" % str(self.impl.__name__)
    rules_dict = self.train([1, 1], 2, 3)
    original = SumAB().GetTargetExpression()
    sol = self.impl.FindLinearCombination(rules_dict, original)
    weights, comps = sol[0], sol[1]
    result = self.impl.SolutionStr(weights, comps)
    for cn in xrange(3):
      for cm in xrange(3):
        n, m = manage.config.N + cn, manage.config.M + cm
        A = np.array(np.random.randn(n, m))
        B = np.array(np.random.randn(n, m))
        print "A", A
        print "B", B
        val_original = eval(original.comp[NUMPY])
        val_result = eval(result[NUMPY])
        dist = abs(val_original - val_result) / abs(val_original)
        self.assertTrue(dist < 1e-3)

  def testdRBM(self):
    print "Running TaylordRBM test for %s" % str(self.impl.__name__)
    self.rbm(power=2, deriv=True, N=3, M=4)

  def testRBM(self):
    print "Running TaylorRBM test for %s" % str(self.impl.__name__)
    self.rbm(power=2, deriv=False, N=2, M=3)
    if self.impl != ExprSymbolic:
      self.rbm(power=3, deriv=False, N=4, M=5)

  def GetNaturalRBMForPower(self, power, N, M):
    rules_dict = self.train([power], N, M)
    result = ""
    original = RBM(power=power, deriv=False).GetTargetExpression()
    sol = self.impl.FindLinearCombination(rules_dict, original)
    weights, comps = sol[0], sol[1]
    result = self.impl.SolutionStrRBM(weights, comps, deriv=False)
    return result[NUMPY]

  def rbm(self, power, deriv, N, M):
    rules_dict = self.train([power], N, M)
    result = ""
    for n in [N, N + 1]:
      for m in [M, M + 1]:
        manage.config.N = n
        manage.config.M = m
        val_original = 0
        W = np.array(np.random.randn(manage.config.N, manage.config.M))
        print "W", W
        if result == "":
          original = RBM(space, power, deriv).GetTargetExpression()
          sol = self.impl.FindLinearCombination(rules_dict, original)
          weights, comps = sol[0], sol[1]
          result = self.impl.SolutionStrRBM(weights, comps, space, deriv)
          print "original comp = %s" % str(original.comp[NUMPY])
          val_original = eval(original.comp[NUMPY])
        else:
          z, dz = Z(W, power)
          if deriv:
            val_original = dz
          else:
            val_original = z
        result[NUMPY] = result[NUMPY].replace("A", "W")
        print str(result[NUMPY])
        print "N = %d, M = %d" % (manage.config.N, manage.config.M)
        ret = eval(result[NUMPY])
        print "val_original = \n%s" % str(val_original)
        print "val_result =\n%s" % str(ret)
        self.assertTrue(val_original.shape == ret.shape)
        self.assertTrue(norm(val_original - ret) / norm(val_original) < 1e-3)

class End2EndZpTests(End2EndTests, unittest.TestCase):
  def __init__(self, *args):
    End2EndTests.__init__(self, ExprZp)
    unittest.TestCase.__init__(self, args[0])

class End2EndSymbolicTests(End2EndTests, unittest.TestCase):
  def __init__(self, *args):
    End2EndTests.__init__(self, ExprSymbolic)
    unittest.TestCase.__init__(self, args[0])

def norm(A):
  ret = np.square(np.sum(np.square(A), keepdims=True))
  if ret.shape == (1, 1):
    return ret[0, 0]
  elif ret.shape == ():
    return ret
  else:
    assert 0

def handler(*_):
  print "Forever is over!"
  raise OSError("end of time")

def main():
  if len(sys.argv) > 1:
    test_name = sys.argv[1]
    single = unittest.TestSuite()
    single.addTest(End2EndZpTests(test_name))
    unittest.TextTestRunner().run(single)
  else:
    unittest.main()

if __name__ == '__main__':
  main()
