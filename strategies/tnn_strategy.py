from manage.scheduler import Scheduler
import numpy as np
import operator
from expr.expr_matrix import ExprMatrix
from tnn import TNN
from collections import defaultdict
import hashlib
from manage.config import APPLIED_RULES
import numpy as np
import copy
import time

class TNNScheduler(Scheduler):
  def __init__(self, params):
    Scheduler.__init__(self, params)
    self.tnn = TNN('tnn_trained/tnn_weights_trained%d.pkl' % (params['run_id']))
    self.target_vec = []
    self.hidden = self.tnn.W[0][0].shape[0]
    np.random.seed(1)
    self.S = np.random.randn(5, 2 * self.hidden) * 0.1
    self.dS = np.zeros_like(self.S)
    self.empty = np.random.randn(self.hidden) * 0.1
    self.lr = 0.1
    self.momentum = 0.5
    self.trained = False
    self.all_data = []
    self.loss = 0
    self.dropout = params['dropout']

  def __str__(self):
    return "TNN_dropout%d" % self.dropout 

  def nonlin_(self, x):
    return np.maximum(x, 0)

  def dnonlin_(self, dX_in, x):
    return dX_in * (x > 0)

  def nonlin(self, x):
    assert(len(x.shape) == 1)
    return self.nonlin_(x)

  def dnonlin(self, (dX_in, x)):
    assert(dX_in.shape == x.shape)
    assert(len(x.shape) == 1)
    return self.dnonlin_(dX_in)

  def softmax_fp(self, x):
    output = x - np.max(x)
    output = np.exp(output)
    output = output / np.sum(output)
    pred = np.argmax(output)
    return output, pred

  def softmax_bp(self, x, y):
    dX = x
    dX[y] -= 1
    return dX

  def predict(self, root, f0, f1):
    if f1 is None:
      f1_ = self.empty
    else:
      f1_ = f1
    f = np.concatenate((f0, f1_))
    output, pred = self.softmax_fp(np.dot(self.S, f))
    self.loss += -np.log(output[root])
    dX_in = self.softmax_bp(output, root)
    self.dS = self.momentum * self.dS + (1 - self.momentum) * np.outer(dX_in, f)
    self.S -= self.lr * self.dS
    self.score += pred == root
    self.all_score += 1

  def tnn_fp(self, x):
    if x is None:
      return self.empty
    elif len(x) == 2:
      root, expr0 = x
      f0 = self.tnn_fp(expr0)
      f0 = f0 * (np.random.randint(0, self.dropout, self.hidden) > 0)
      self.predict(root, f0, None)
      return self.nonlin(np.dot(self.tnn.W[root][0], f0))
    elif len(x) == 3:
      root, expr0, expr1 = x
      f0 = self.tnn_fp(expr0)
      f1 = self.tnn_fp(expr1)
      f0 = f0 * (np.random.randint(0, self.dropout, self.hidden) > 0)
      f1 = f1 * (np.random.randint(0, self.dropout, self.hidden) > 0)
      self.predict(root, f0, f1)
      f_tmp = np.tensordot(self.tnn.W[root][0], f0, axes=(2, 0))
      f = np.dot(f_tmp, f1)
      return self.nonlin(f)

  def Train(self, data):
    print "data", data
    if data is not None:
      self.all_data.append(data)
    if len(self.all_data) == 0:
      return
    self.dS[:] = 0
    self.score = 0
    self.all_score = 1
    loss = [float('Inf'), 1e10] 
    bestS = None
    start = time.time()
    while ((max(loss[-100:]) > min(loss[-10:]) and len(loss) < 5e3) or len(loss) < 1e3) and (time.time() - start) < 5 * 60:
      self.score = 0
      self.all_score = 0
      self.loss = 0
      for d in self.all_data[-1]:
        self.tnn_fp(d)
      acc = float(self.score) / float(self.all_score)
      self.loss /= self.all_score
      loss.append(self.loss)
      if len(loss) % 500 == 3:
        print "Iter = %d, Training acc = %f = %d / %d, nats = %f" % (len(loss), acc, self.score, self.all_score, np.exp(loss[-1]))
      if loss[-1] <= min(loss):
        bestS = copy.copy(self.S)
    self.S = copy.copy(bestS)
    print "Final acc = %f, loss = %f, nats = %.20f" % (acc, loss[-1], np.exp(min(loss)))
    self.trained = True

  def GetEval(self, rule, expr1, expr2):
    if not self.trained:
      return 1
    f1 = None
    f2 = self.tnn.W[-1][0]
    ops = expr1.ops
    if expr1.tnn_vec is None:
      expr1.tnn_vec = self.tnn.tnn_fp(expr1.comp[APPLIED_RULES])[0]
    f1 = expr1.tnn_vec
    if expr2 is not None:
      ops += expr2.ops
      if expr2.tnn_vec is None:
        expr2.tnn_vec = self.tnn.tnn_fp(expr2.comp[APPLIED_RULES])[0]
      f2 = expr2.tnn_vec
    
    f = np.concatenate((f1, f2))
    output, pred = self.softmax_fp(np.dot(self.S, f))
    c = -output[rule.idx]
    return c
