#!/usr/bin/python
import sys
import os
sys.path.insert(0, '../')
import unittest
import numpy as np
import manage.config
import manage.solver as solver
from fractions import Fraction as F
from strategies.ngram import NgramScheduler
from targets.sum_AAT import SumAAT
from targets.sum_AB import SumAB
from targets.sum_AmultA import SumAmultA
from targets.rbm import RBM
from targets.sym import Sym
from targets.rbm_oneside import RBMOneSide
from expr.expr_zp import ExprZp
from manage.config import MATLAB
from main import execute

class MatlabEvaluationTests(unittest.TestCase):

  def testEquivalence(self):
    targets = [RBMOneSide, SumAmultA, RBM, SumAAT, SumAB, Sym]
    for target in targets:
      manage.config.EXPR_IMPL = ExprZp
      scheduler = NgramScheduler
      params = {'depth': 5, 'trials': 1}
      matlab = execute(scheduler, params, target, maxpower=4, record_it=False)[0]["matlab"]
      for i, m in enumerate(matlab):
        f = open('code.m', 'w')
        original = target(i + 1).GetTargetExpression()
        code = ""
        code += original.comp[MATLAB] + "\n"
        code += "optimized = "
        expr = ""
        for w, c in m:
          if len(expr) > 0:
            expr += " + "
          expr += "%s * (%s)" % (ExprZp.ToFrac(w), c)
        if target == RBM:
          expr = "2^(n + m - %d) * (%s)" % (manage.config.N + manage.config.M, expr)
        if target == RBMOneSide:
          expr = "2^(n - %d) * (%s)" % (manage.config.M, expr)
        code += expr + ";\n"
        code += "assert(sum(abs(original(:) - optimized(:))) / sum(abs(original(:))) < 1e-8);"
        f.write(code)
        f.close()
        print "Executing matlab code: \n%s\n" % code
        ret = os.system("matlab -nodesktop -nodisplay -nojvm -nosplash -r \"try run('code.m');catch exit(-1); end; exit(0) \" > /dev/null")
        if ret == 0:
          print "Passed matlab verification\n"
        else:
          self.assertEquals(ret, 0)
        os.remove('code.m')

def main():
  unittest.main()

if __name__ == '__main__':
  main()
