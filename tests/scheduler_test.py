import unittest
import  manage.config
from expr.expr_symbolic import ExprSymbolic
from expr.expr_zp import ExprZp
from targets.target import Target
from strategies.brute_force import BruteForceScheduler
from  manage.config import THIS
import numpy as np

class SchedulerTests(unittest.TestCase):

  def testSumOfSquareResult(self):
    manage.config.N = 2
    manage.config.M = 3
    manage.config.MAXPOWER = np.array([2])
    manage.config.EXPR_IMPL = ExprSymbolic
    sched = BruteForceScheduler()
    target_expr = Target(sched)
    target_expr.SetStartSymbols(1)
    sched.SetTarget(target_expr)
    sched.Run()
    rules_dict = sched.cache.GetExpressions((1, 1)).values()
    sum_of_squares = False
    A = target_expr.start_symbols[0]
    print A
    for r in rules_dict:
      matrix = eval(r.comp[THIS])
      self.assertEqual(matrix, r)
      e = r.expressions[0, 0]
      sum_of_squares |= (
          all(1 == p for p in e.quants) and
          ((e.expr_vectors == 2) + (e.expr_vectors == 0)).all())
    self.assertTrue(sum_of_squares)

  def testSelfComputation(self):
    manage.config.N = 2
    manage.config.M = 3
    manage.config.MAXPOWER = np.array([2])
    manage.config.EXPR_IMPL = ExprZp
    sched = BruteForceScheduler()
    target_expr = Target(sched)
    target_expr.SetStartSymbols(1)
    sched.SetStartExpressions(target_expr)
    rules_dict = sched.cache.GetExpressions((1, 1)).values()
    A = target_expr.start_symbols[0]
    print A
    for r in rules_dict:
      matrix = eval(r.comp[THIS])
      self.assertEqual(matrix, r)


def main():
  unittest.main()

if __name__ == '__main__':
  main()
