import unittest
import copy
import numpy as np
from expr.expr_symbolic import ExprSymbolic
from expr.expr_matrix import ExprMatrix
import tests.expr_testutils as expr_testutils
import manage.config
from manage.config import NUMPY

class ExprMatrixSymbolicTests(unittest.TestCase):


  # XXXXX : finish broadcasting test.
  def testFindLinearCombinationBroadcasting(self):
    manage.config.MAXPOWER = np.array([10])
    #  mat1          mat2         target
    #  x1  | x1x2    x1           3x1      | 2x1x2 + x1
    #  2x3 | x2^2    x3           5x3      | 2x2^2 + x3
    mat1_11 = ExprSymbolic([1], np.array([[1, 0, 0]]))
    mat1_12 = ExprSymbolic([1], np.array([[1, 1, 0]]))
    mat1_21 = ExprSymbolic([2], np.array([[0, 0, 1]]))
    mat1_22 = ExprSymbolic([1], np.array([[0, 2, 0]]))

    mat2_11 = ExprSymbolic([1], np.array([[1, 0, 0]]))
    mat2_21 = ExprSymbolic([1], np.array([[0, 0, 1]]))

    target_11 = ExprSymbolic([3], np.array([[1, 0, 0]]))
    target_12 = ExprSymbolic([2, 1], np.array([[1, 1, 0], [1, 0, 0]]))
    target_21 = ExprSymbolic([5], np.array([[0, 0, 1]]))
    target_22 = ExprSymbolic([2, 1], np.array([[0, 2, 0], [0, 0, 1]]))

    mat1 = ExprMatrix("a",
        np.array([[mat1_11, mat1_12], [mat1_21, mat1_22]]), np.array([1]))
    mat2 = ExprMatrix("b",
        np.array([[mat2_11], [mat2_21]]), np.array([1]))
    target = ExprMatrix(
        "target",
        np.array([[target_11, target_12], [target_21, target_22]]),
        np.array([1]))
    expressions_list = [mat1, mat2]
    weights = ExprSymbolic.FindLinearCombination(expressions_list, target)[0]

    self.assertEquals(2, len(weights))
    self.assertAlmostEqual(2.0, weights[0])
    self.assertAlmostEqual(1.0, weights[1])


  def testFindLinearCombinationWithMatrix(self):
    manage.config.MAXPOWER = np.array([10])
    #  mat1          mat2         target
    #  x1  | x1x2    x1 | x1x2    3x1      | 3x1x2
    #  2x3 | x2^2    x1 | x3      4x3+x1   | 2x2^2 + x3
    mat1_11 = ExprSymbolic([1], np.array([[1, 0, 0]]))
    mat1_12 = ExprSymbolic([1], np.array([[1, 1, 0]]))
    mat1_21 = ExprSymbolic([2], np.array([[0, 0, 1]]))
    mat1_22 = ExprSymbolic([1], np.array([[0, 2, 0]]))

    mat2_11 = ExprSymbolic([1], np.array([[1, 0, 0]]))
    mat2_12 = ExprSymbolic([1], np.array([[1, 1, 0]]))
    mat2_21 = ExprSymbolic([1], np.array([[1, 0, 0]]))
    mat2_22 = ExprSymbolic([1], np.array([[0, 0, 1]]))

    target_11 = ExprSymbolic([3], np.array([[1, 0, 0]]))
    target_12 = ExprSymbolic([3], np.array([[1, 1, 0]]))
    target_21 = ExprSymbolic([4, 1], np.array([[0, 0, 1], [1, 0, 0]]))
    target_22 = ExprSymbolic([2, 1], np.array([[0, 2, 0], [0, 0, 1]]))

    mat1 = ExprMatrix("a",
        np.array([[mat1_11, mat1_12], [mat1_21, mat1_22]]), np.array([1]))
    mat2 = ExprMatrix("b",
        np.array([[mat2_11, mat2_12], [mat2_21, mat2_22]]), np.array([1]))
    target = ExprMatrix(
        "target",
        np.array([[target_11, target_12], [target_21, target_22]]),
        np.array([1]))
    expressions_list = [mat1, mat2]
    weights = ExprSymbolic.FindLinearCombination(expressions_list, target)[0]

    self.assertEquals(2, len(weights))
    self.assertAlmostEqual(2.0, weights[0])
    self.assertAlmostEqual(1.0, weights[1])

  def testHashImmuneToConst(self):
    manage.config.MAXPOWER = np.array([10])
    a = ExprSymbolic([2, 3],
        np.array([[1, 2, 3], [4, 5, 6]]))
    b = ExprSymbolic([4, 6],
        np.array([[1, 2, 3], [4, 5, 6]]))
    self.assertNotEquals(a, b)
    a = ExprMatrix("a", np.array([[a]]), np.array([1]))
    b = ExprMatrix("b", np.array([[b]]), np.array([1]))
    self.assertEquals(a, b)

  def testAddOne(self):
    manage.config.MAXPOWER = np.array([10])
    a = ExprSymbolic([5], np.array([[0, 0, 0, 0]]))
    expressions = np.array([[a]], dtype=np.object)
    matrix = ExprMatrix('A', expressions, powers=np.array([1]))
    self.assertTrue(matrix.Add(4).expressions[0, 0].quants.shape[0] == 1)

  def testSubMatrices(self):
    n = 2
    m = 3
    A = np.array(np.random.randn(n, m))
    B = np.array(np.random.randn(n, m))
    print A
    print B
    C, D = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprSymbolic)
    E = D.Marginalize(axis=0).Marginalize(axis=1)
    val_E = eval(E.comp[NUMPY])
    D = D.Sub(C)
    C = C.Marginalize(axis=0).Marginalize(axis=1)
    D = D.Marginalize(axis=0).Marginalize(axis=1)
    self.assertNotEquals(C, D)
    val_C = eval(C.comp[NUMPY])
    val_D = eval(D.comp[NUMPY])
    print D.comp
    self.assertTrue(abs(val_E - val_C - val_D) < 1e-4)

  def testAddSubNumber(self):
    n = 2
    m = 3
    C = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprSymbolic)[0]
    D = C.Add(10)
    D = D.Sub(4)
    C = C.Marginalize(axis=0).Marginalize(axis=1)
    D = D.Marginalize(axis=0).Marginalize(axis=1)
    self.assertNotEquals(C, D)
    A = np.array(np.random.randn(n, m))
    print A
    val_C = eval(C.comp[NUMPY])
    val_D = eval(D.comp[NUMPY])
    self.assertTrue(abs(val_C + 6 * 2 * 3 - val_D) < 1e-4)

  def testMultiplyNumber(self):
    n = 2
    m = 3
    C = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprSymbolic)[0]
    D = C.ElementwiseMultiply(10)
    C = C.Marginalize(axis=0).Marginalize(axis=1)
    D = D.Marginalize(axis=0).Marginalize(axis=1)
    print "C", C
    print "D", D
    self.assertEquals(C, D)
    A = np.array(np.random.randn(n, m))
    print A
    val_C = eval(C.comp[NUMPY])
    val_D = eval(D.comp[NUMPY])
    self.assertTrue(abs(10 * val_C - val_D) < 1e-4)

  def testSameHash(self):
    manage.config.MAXPOWER = np.array([10])
    a = ExprSymbolic([1], np.array([[1, 0, 0, 0]]))
    b = ExprSymbolic([1], np.array([[0, 1, 0, 0]]))
    c = ExprSymbolic([1], np.array([[0, 0, 1, 0]]))
    d = ExprSymbolic([1], np.array([[0, 0, 0, 1]]))
    expressions = np.array([[a, b], [c, d]], dtype=np.object)

    matrix = ExprMatrix('A', expressions, powers=np.array([1]))
    Q = matrix.Marginalize(axis=0).Marginalize(axis=1)
    W = matrix.Marginalize(axis=1).Marginalize(axis=0)
    self.assertEquals(Q, W)

  def testMarginalizeBothAxis(self):
    a = ExprSymbolic([1], np.array([[1, 0, 0]]))
    b = ExprSymbolic([1], np.array([[0, 1, 0]]))
    c = ExprSymbolic([2], np.array([[0, 0, 1]]))
    expressions = np.array([[a, b, c], [a, b, c]], dtype=np.object)

    matrix = ExprMatrix('A', expressions, powers=np.array([1]))
    matrix = matrix.Marginalize(axis=None)
    self.assertEquals((1, 1), matrix.expressions.shape)
    self.assertEquals(3, len(matrix.expressions.item(0, 0).quants))
    self.assertEquals([2, 2, 4], sorted(matrix.expressions.item(0, 0).quants))

  def testElementwiseMultiply(self):
    manage.config.MAXPOWER = np.array([10, 10])
    # a = x1 * x3
    # b = x1 * x2^2
    # c = x2^3 + x3^4
    a = ExprSymbolic([1], np.array([[1, 0, 1]]))
    b = ExprSymbolic([1], np.array([[1, 2, 0]]))
    c = ExprSymbolic([1, 1], np.array([[0, 3, 0], [0, 0, 4]]))
    expressions1 = np.array([[a, b], [c, a]])
    expressions2 = np.array([[a, a], [a, a]])
    # mat1:
    #  x1x3  |  x1 * x2^2
    #  x2^3 + x3^4 | x1x3
    mat1 = ExprMatrix('M1', expressions1, powers=np.array([1, 0]))
    mat2 = ExprMatrix('M2', expressions2, powers=np.array([0, 1]))

    mat1 = mat1.ElementwiseMultiply(mat2)
    self.assertEquals((2, 2), mat1.expressions.shape)

    elem = mat1.expressions[0, 0]
    self.assertEquals(1, elem.expr_vectors.shape[0])
    self.assertEquals(1, elem.quants[0])
    self.assertTrue((np.array([2, 0, 2]) == elem.expr_vectors).all())

    elem2 = mat1.expressions[1, 0]  # x1x3 * (x2^3 + x3^4)
    self.assertEquals(2, elem2.expr_vectors.shape[0])
    self.assertTrue((np.array([1, 3, 1]) == elem2.expr_vectors).any())
    self.assertTrue((np.array([1, 0, 5]) == elem2.expr_vectors).any())
    self.assertTrue((np.array([1, 1]) == elem2.quants).any())

  def testShapesAfterSumAreCorrec(self):
    a = ExprSymbolic([1], np.array([[1, 0, 0]]))
    b = ExprSymbolic([1], np.array([[0, 1, 0]]))
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

  def testNoHashCollision(self):
    n = 2
    m = 3
    A, B = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprSymbolic)
    B = B.Transpose()

    A1 = copy.copy(A)
    B1 = copy.copy(B)
    B1 = B1.Marginalize(axis=1)
    A1 = A1.Multiply(B1)
    A1 = A1.Marginalize(axis=0)
    s1 = ('(np.sum((np.dot(A, (np.sum((B.transpose()), axis=1, '
        'keepdims=True)))), axis=0, keepdims=True))')
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
    self.assertNotEquals(len(A1.expressions[0, 0].quants),
                         len(B2.expressions[0, 0].quants))
    self.assertNotEquals(A1, B2)

  def testNoHashCollisionAfterTranspose(self):
    n = 2
    m = 3
    _, B = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprSymbolic)
    X = B.Marginalize(axis=1)
    Y = (B.Marginalize(axis=1)).Transpose()
    self.assertNotEquals(X, Y)

  def testNoHashCollisionTwoMatricesWithOne(self):
    # (((B.sum(axis=1)) * (A.sum(axis=0))).sum(axis=1))
    n = 2
    m = 3
    A, B = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprSymbolic)
    X = B.Marginalize(axis=1)
    Y = A.Marginalize(axis=0)
    Z = (X.Multiply(Y)).Marginalize(axis=1)
    self.assertNotEquals(X, Z)

  def testSumMultiplyWorks(self):
    n = 2
    m = 3
    A = expr_testutils.GetMatricesSumMul(n, m, expr_impl=ExprSymbolic)[0]
    B = A.Marginalize(axis=0)
    B = B.Marginalize(axis=1)
    A = A.Marginalize(axis=0)
    A = A.Marginalize(axis=1)
    self.assertEquals(A, B)

def main():
  unittest.main()

if __name__ == '__main__':
  main()
