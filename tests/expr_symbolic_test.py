import unittest
import numpy as np
from expr.expr_symbolic import ExprSymbolic
import manage.config
from fractions import Fraction as F

class ExprSymbolicTests(unittest.TestCase):

  def testDiffHash(self):
    a = ExprSymbolic([F(2, 7), F(3, 11)], np.array([[1, 0, 0], [0, 1, 0]]))
    b = ExprSymbolic([F(2, 13), F(3, 19)], np.array([[1, 0, 0], [0, 1, 0]]))
    self.assertNotEquals(a, b)

  def testAddQExpressions(self):
    a = ExprSymbolic([F(1, 2), F(1, 100)], np.array([[1, 0, 0], [0, 1, 0]]))
    b = ExprSymbolic([F(1, 3)], np.array([[1, 0, 0]]))
    c = ExprSymbolic([F(5, 6), F(2, 200)], np.array([[1, 0, 0], [0, 1, 0]]))
    d = a + b
    self.assertEquals(d, c)

  def testAddExpressions(self):
    a = ExprSymbolic([1], np.array([[1, 0, 0]]))
    b = ExprSymbolic([1], np.array([[0, 1, 0]]))
    c = ExprSymbolic([2], np.array([[1, 0, 0]]))
    d = a + b + c
    print d.quants
    self.assertEquals(2, len(d.quants))
    self.assertTrue(3 in d.quants)
    self.assertTrue(1 in d.quants)

  def testMatlabImplAddExpression(self):
    a = ExprSymbolic([3, 5, 4],
        np.array([[1, 2, 3, 0], [0, 2, 3, 5], [0, 0, 1, 0]]))
    b = ExprSymbolic([6, 7], np.array([[0, 2, 3, 5], [0, 1, 0, 0]]))
    c = a + b
    self.assertEquals(4, len(c.expr_vectors))
    self.assertEquals([3, 4, 7, 11], sorted(c.quants))

  def testSmallMultiplication(self):
    a = ExprSymbolic([1], np.array([[1, 2, 3]]))
    b = ExprSymbolic([2], np.array([[3, 3, 3]]))
    c = a * b
    self.assertEquals(1, len(c.expr_vectors))
    self.assertTrue(2 in c.quants)
    self.assertTrue((np.array([4, 5, 6]) == c.expr_vectors[0]).all())

  def testMatlabImplMultiplyExpression(self):
    a = ExprSymbolic([3, 5, 4],
        np.array([[1, 2, 3, 0], [0, 2, 3, 5], [0, 0, 1, 0]]))
    b = ExprSymbolic([6, 7], np.array([[0, 2, 3, 5], [0, 1, 0, 0]]))
    c = a * b
    self.assertEquals(6, len(c.expr_vectors))
    self.assertEquals(sorted([28, 21, 35, 24, 18, 30]), sorted(c.quants))


  def testMatlabImplManyAddExpressions(self):
    a = ExprSymbolic([3, 5, 4],
        np.array([[1, 2, 3, 0], [0, 2, 3, 5], [0, 0, 1, 0]]))
    b = ExprSymbolic([6, 7], np.array([[0, 2, 3, 5], [0, 1, 0, 0]]))
    c = ExprSymbolic.AddManyExpressions([a, a, b, b])
    self.assertEquals(4, len(c.expr_vectors))
    # 2 *[3, 4, 7, 11]==[6, 8, 14, 22]
    self.assertEquals([6, 8, 14, 22], sorted(c.quants))

  def testHashIsComputed(self):
    a = ExprSymbolic([2, 3],
        np.array([[1, 2, 3], [4, 5, 6]]))
    b = ExprSymbolic([2, 2],
        np.array([[1, 2, 3], [4, 5, 6]]))
    self.assertNotEquals(a, b)

def main():
  unittest.main()

if __name__ == '__main__':
  main()
