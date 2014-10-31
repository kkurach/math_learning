import copy
import tests.expr_testutils as expr_testutils
import numpy as np
import unittest

from expr.expr_zp import ExprZp
from expr.expr_matrix import ExprMatrix
import manage.config
from manage.config import NUMPY

class ExprMatrixZpTests(unittest.TestCase):

  def testMarginalizeBothAxis(self):
    manage.config.MAXPOWER = np.array([10])
    a = ExprZp([1], np.array([[1, 0, 0]]))
    b = ExprZp([1], np.array([[0, 1, 0]]))
    c = ExprZp([2], np.array([[0, 0, 1]]))
    expressions = np.array([[a, b, c], [a, b, c]], dtype=np.object)

    matrix = ExprMatrix('A', expressions, powers=np.array([1]))
    matrix = matrix.Marginalize(axis=None)
    self.assertEquals((1, 1), matrix.expressions.shape)

  def testElementwiseMultiply(self):
    manage.config.MAXPOWER = np.array([10, 10])
    # a = x1 * x3
    # b = x1 * x2^2
    # c = x2^3 + x3^4
    a = ExprZp([1], np.array([[1, 0, 1]]))
    b = ExprZp([1], np.array([[1, 2, 0]]))
    c = ExprZp([1, 1], np.array([[0, 3, 0], [0, 0, 4]]))
    expressions1 = np.array([[a, b], [c, a]])
    expressions2 = np.array([[a, a], [a, a]])
    # mat1:
    #  x1x3  |  x1 * x2^2
    #  x2^3 + x3^4 | x1x3
    mat1 = ExprMatrix('M1', expressions1, powers=np.array([1, 0]))
    mat2 = ExprMatrix('M2', expressions2, powers=np.array([0, 1]))

    mat1.ElementwiseMultiply(mat2)
    self.assertEquals((2, 2), mat1.expressions.shape)

  def testShapesAfterSumAreCorrec(self):
    manage.config.MAXPOWER = np.array([10])
    a = ExprZp([1], np.array([[1, 0, 0]]))
    b = ExprZp([1], np.array([[0, 1, 0]]))
    expressions = np.array([[a, a, a], [b, b, b]])
    matrix = ExprMatrix('M', expressions, powers=np.array([1]))
    # Exp matrix test
    self.assertEquals((2, 3), matrix.expressions.shape)
    m0 = copy.copy(matrix)
    m0 = m0.Marginalize(axis=0)
    self.assertEquals((1, 3), m0.expressions.shape)
    self.assertEquals(a + b, m0.expressions[0, 0])
    self.assertEquals(a + b, m0.expressions[0, 1])

    m1 = copy.copy(matrix)
    m1 = m1.Marginalize(axis=1)
    self.assertEquals((2, 1), m1.expressions.shape)
    self.assertEquals(a + a + a, m1.expressions[0, 0])
    self.assertEquals(b + b + b, m1.expressions[1, 0])

  def testEnd2EndNoHashCollision(self):
    n = 2
    m = 3
    A, B = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprZp)
    B = B.Transpose()

    A1 = copy.copy(A)
    B1 = copy.copy(B)
    B1 = B1.Marginalize(axis=1)
    A1 = A1.Multiply(B1)
    A1 = A1.Marginalize(axis=0)
    s1 = ('(np.sum((np.dot(A, (np.sum((B.transpose()), axis=1,'
        ' keepdims=True)))), axis=0, keepdims=True))')
    self.assertEquals(s1, A1.comp[NUMPY])

    A2 = copy.copy(A)
    B2 = copy.copy(B)
    A2 = A2.Marginalize(axis=1)
    B2 = B2.Marginalize(axis=0)
    B2 = B2.Multiply(A2)
    s2 = ('(np.dot((np.sum((B.transpose()), axis=0, keepdims=True)),'
        ' (np.sum(A, axis=1, keepdims=True))))')
    self.assertEquals(s2, B2.comp[NUMPY])
    self.assertEquals((1, 1), A1.expressions.shape)
    self.assertEquals((1, 1), B2.expressions.shape)
    print "DEBUG:"
    print A1.expressions[0, 0].PrintDebug()
    print B2.expressions[0, 0].PrintDebug()
    self.assertNotEquals(A1, B2)

  # TODO(wojtas): add proper assert here or remove function
  def testSumMultiplyWorks(self):
    n = 2
    m = 3
    A, B = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprZp)
    B = B.Transpose()
    #A.PrintDebug()
    #B.PrintDebug()
    B.Marginalize(axis=0)
    A.Marginalize(axis=1)
    #A.PrintDebug()
    #B.PrintDebug()
    A.Multiply(B)
    #A.PrintDebug()
    self.assertEquals(1, 1)

def main():
  unittest.main()

if __name__ == '__main__':
  main()
