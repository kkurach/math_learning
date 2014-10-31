import unittest
import numpy as np
import manage.config
import manage.solver as solver
from fractions import Fraction as F

class SolverTests(unittest.TestCase):

  def testFracGauss(self):
    mapF = lambda x: map(F, x)
    A = np.array(map(mapF, [[96, 16, 16, 16, 16], [1, 0, 0, 0, 0]])).transpose()
    b = np.array(map(F, [24, 8, 8, 8, 8]))
    x = solver.Solver.GaussF(A, b)
    self.assertTrue(x[0] == F(1, 2))
    self.assertTrue(x[1] == F(-24))

  def testRBMGauss(self):
    A = np.array([[6, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0]]).transpose()
    b = np.array([24, 8, 8, 8, 8, 8, 8])
    x = solver.Solver.GaussP(A, b)
    x[x > manage.config.PRIME / 2] -= manage.config.PRIME
    self.assertTrue((np.array([8, -24]) == x).all())

  def testGauss(self):
    A = np.array([[1, 3, 7], [4, 0, 14], [2, 6, 8]])
    b = np.array([0, 1, 2])
    original_prime = manage.config.PRIME
    manage.config.PRIME = 19
    x = solver.Solver.GaussP(A, b)
    manage.config.PRIME = original_prime
    self.assertTrue((np.array([3, 4, 6]) == x).all())

def main():
  unittest.main()

if __name__ == '__main__':
  main()
