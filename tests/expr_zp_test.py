import unittest
import numpy as np
from expr.expr_zp import ExprZp
from expr.expr_matrix import ExprMatrix
import manage.config

class ExprZpTests(unittest.TestCase):

  def testAddExpressions(self):
    a = ExprZp([1], np.array([[1, 0, 0]])) # x1
    b = ExprZp([1], np.array([[0, 0, 1]])) # x3
    c = ExprZp([2], np.array([[1, 0, 1]])) # 2x1x3
    d = ExprZp([2], np.array([[1, 0, 0]])) # 2x1
    e = ExprZp([2], np.array([[0, 0, 1]])) # 2x3
    self.assertEquals(a + a, d)
    self.assertEquals(b+b, e)
    print 'Karol D:'
    d.PrintDebug()
    print 'Karol E:'
    e.PrintDebug()
    print 'Karol D*E:'
    (d*e).PrintDebug()
    print 'Karol C+C:'
    (c+c).PrintDebug()
    self.assertEquals(d * e, c+c)

  def testHashIsComputed(self):
    manage.config.MAXPOWER = np.array([10])
    a = ExprZp(
        [2, 3],
        np.array([[1, 2, 3], [4, 5, 6]]))
    b = ExprZp(
        [2, 2],
        np.array([[1, 2, 3], [4, 5, 6]]))
    self.assertNotEquals(a, b)
    a = ExprMatrix("a", np.array([[a]]), np.array([1]))
    b = ExprMatrix("b", np.array([[b]]), np.array([1]))
    self.assertNotEquals(a, b)

  def testHashImmuneToConst(self):
    manage.config.MAXPOWER = np.array([10])
    a = ExprZp(
        [2, 3],
        np.array([[1, 2, 3], [4, 5, 6]]))
    b = ExprZp(
        [4, 6],
        np.array([[1, 2, 3], [4, 5, 6]]))
    self.assertNotEquals(a, b)
    a = ExprMatrix("a", np.array([[a]]), np.array([1]))
    b = ExprMatrix("b", np.array([[b]]), np.array([1]))
    self.assertEquals(a, b)

  def testFindLinearCombinationWithMatrix(self):
    manage.config.MAXPOWER = np.array([10])
    #  mat1          mat2         target
    #  x1  | x1x2    x1 | x1x2    3x1      | 3x1x2
    #  2x3 | x2^2    x1 | x3      4x3+x1   | 2x2^2 + x3
    mat1_11 = ExprZp([1], np.array([[1, 0, 0]]))
    mat1_12 = ExprZp([1], np.array([[1, 1, 0]]))
    mat1_21 = ExprZp([2], np.array([[0, 0, 1]]))
    mat1_22 = ExprZp([1], np.array([[0, 2, 0]]))

    mat2_11 = ExprZp([1], np.array([[1, 0, 0]]))
    mat2_12 = ExprZp([1], np.array([[1, 1, 0]]))
    mat2_21 = ExprZp([1], np.array([[1, 0, 0]]))
    mat2_22 = ExprZp([1], np.array([[0, 0, 1]]))

    target_11 = ExprZp([3], np.array([[1, 0, 0]]))
    target_12 = ExprZp([3], np.array([[1, 1, 0]]))
    target_21 = ExprZp([4, 1], np.array([[0, 0, 1], [1, 0, 0]]))
    target_22 = ExprZp([2, 1], np.array([[0, 2, 0], [0, 0, 1]]))

    mat1 = ExprMatrix("a",
        np.array([[mat1_11, mat1_12], [mat1_21, mat1_22]]), np.array([1]))
    mat2 = ExprMatrix("b",
        np.array([[mat2_11, mat2_12], [mat2_21, mat2_22]]), np.array([1]))
    target = ExprMatrix(
        "target",
        np.array([[target_11, target_12], [target_21, target_22]]),
        np.array([1]))
    expressions_list = [mat1, mat2]
    weights = ExprZp.FindLinearCombination(expressions_list, target)[0]

    self.assertEquals(2, len(weights))
    self.assertAlmostEqual(2.0, weights[0])
    self.assertAlmostEqual(1.0, weights[1])

def main():
  unittest.main()

if __name__ == '__main__':
  main()
