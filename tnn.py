#!/usr/bin/python
import os
import numpy as np
import copy
import math
import cPickle
import os.path
import os

GC = False#True

def norm(x):
  return np.sqrt(np.sum(np.square(x)))

def assert_close(a, b):
  if norm(a) < 1e-5 and norm(b) < 1e-5:
    return
  diff = norm(a - b.reshape(a.shape)) / norm(b) 
  if diff > 1e-4 or math.isnan(diff):
    print "diff = %f, norm(a) = %f, norm(b) = %f" % (diff, norm(a), norm(b))
    a = a.reshape(np.prod(a.shape))
    b = b.reshape(np.prod(b.shape))
    print "a = \n%s" % str(a)
    print "b = \n%s" % str(b)
    assert(0)

class TNN(object):
  def __init__(self, fname='tnn_weights.pkl', seed=1):
    self.W = []
    if GC:
      self.hidden = 5
    else:
      self.hidden = 30
    self.seed = seed
    self.lr = 0.01
    self.momentum = 0.9
    self.init(3)
    self.fname = fname
    self.scores = []
    self.load()

  def arity(self, data):
    s = set()
    if type(data) is list:
      for d in data:
        s = s.union(self.arity(d))
    elif data is not None:
      if len(data) == 2:
        root, expr1 = data
        s.add((root, 2))
        s = s.union(self.arity(expr1))
      else:
        root, expr1, expr2 = data
        s.add((root, 3))
        s = s.union(self.arity(expr1))
        s = s.union(self.arity(expr2))
    return s

  def nonlin_(self, x):
    return np.maximum(x, 0)

  def dnonlin_(self, dX_in, x):
    return dX_in * (x > 0)

  def nonlin(self, x):
    assert(len(x[0].shape) == 1)
    return self.nonlin_(x[0]), x

  def dnonlin(self, (dX_in, x)):
    assert(dX_in.shape == x[0].shape)
    assert(len(x[0].shape) == 1)
    return self.dnonlin_(dX_in, x[0]), x[1]

  def single_fp(self, root, f0, f1=None):
    f = None
    if f1 is None:
      return self.nonlin_(np.dot(self.W[root][0], f0))
    else:
      f_tmp = np.tensordot(self.W[root][0], f0, axes=(2, 0))
      return self.nonlin_(np.dot(f_tmp, f1))

  def tnn_fp(self, x):
    if x is None:
      return (self.W[-1][0],)
    elif len(x) == 2:
      root, expr0 = x
      f0 = self.tnn_fp(expr0)
      return self.nonlin((np.dot(self.W[root][0], f0[0]), f0))
    elif len(x) == 3:
      root, expr0, expr1 = x
      f0 = self.tnn_fp(expr0)
      f1 = self.tnn_fp(expr1)
      f_tmp = np.tensordot(self.W[root][0], f0[0], axes=(2, 0))
      f = np.dot(f_tmp, f1[0])
      return self.nonlin((f, f0, f1))

  def tnn_bp(self, (dX_in, x), data):
    global W
    if data is None:
      self.W[-1][1] += dX_in
      return
    dX_in, x = self.dnonlin((dX_in, x))
    if len(data) == 2:
      assert(len(x) == 2)
      self.W[data[0]][1] += np.outer(dX_in, x[1][0])
      dX = np.dot(self.W[data[0]][0].transpose(), dX_in)
      self.tnn_bp((dX, x[1]), data[1])
    elif len(data) == 3:
      assert(len(x) == 3)
      dX_r = dX_in.reshape(list(dX_in.shape) + [1])
      o = np.outer(x[2][0], x[1][0])
      o = o.reshape(list(o.shape) + [1])
      self.W[data[0]][1] += np.tensordot(dX_r, o, axes=(1, 2))
      dX0 = np.dot(np.tensordot(self.W[data[0]][0], x[2][0], axes=(1, 0)).transpose(), dX_in)
      self.tnn_bp((dX0, x[1]), data[1])
      dX1 = np.dot(np.tensordot(self.W[data[0]][0], x[1][0], axes=(2, 0)).transpose(), dX_in)
      self.tnn_bp((dX1, x[2]), data[2])

  def lin_fp(self, x):
    return np.dot(self.W[-2][0], x[0]), x

  def lin_bp(self, (dX_in, x)):
    dX = np.dot(self.W[-2][0].transpose(), dX_in)
    self.W[-2][1] = np.outer(dX_in, x[1][0])
    return dX, x[1]

  def softmax_fp(self, x):
    output = x[0] - np.max(x[0])
    output = np.exp(output)
    output = output / np.sum(output)
    pred = np.argmax(output)
    return (output, x), pred

  def softmax_bp(self, x, y):
    dX = x[0]
    dX[y] -= 1
    return dX, x[1]

  def init(self, depth):
    size = 0
    np.random.seed(self.seed)
    path = "training/%d/" % depth
    files = os.listdir(path)
    train_data = []
    test_data = []
    classes = 0
    for d in files:
      same = []
      with open(path + d, 'r') as f:
        lines = f.readlines()
        for l in lines:
          l = eval(l)
          same.append(l)
      if len(same) >= 10:
        classes += 1
        train_data.append(same[2:])
        test_data.append(same[0:2])
        size += len(same)
    print "Number of classes = %d, size = %d,  depth = %d" % (classes, size, depth)
    self.init_weights(train_data)
    return train_data, test_data

  def init_weights(self, train_data):
    if len(self.W) > 0:
      return
    classes = len(train_data)
    ar = sorted(self.arity(train_data))
    for i in xrange(len(ar)):
      s = [self.hidden] * ar[i][1]
      print "Size of %d is %s" % (i, str(s))
      triplet = [np.random.randn(*s) * 0.001, \
                 np.zeros(tuple(s)),\
                 np.zeros(tuple(s))]
      self.W.append(triplet)
      for j in xrange(self.hidden):
        idx = [j] * ar[i][1]
        self.W[-1][0][tuple(idx)] += 1
    self.W.append([None, None, None])
    self.W.append([np.sort(np.random.randn(self.hidden)),
                   np.zeros(self.hidden),
                   np.zeros(self.hidden)])
    self.reset_target_matrix(train_data)

  def reset_target_matrix(self, train_data):
    classes = len(train_data)
    self.W[-2][0] = np.random.randn(classes, self.hidden) * 0.1
    self.W[-2][1] = np.zeros_like(self.W[-2][0])
    self.W[-2][2] = np.zeros_like(self.W[-2][0])

  def fp(self, d):
    return self.softmax_fp(self.lin_fp(self.tnn_fp(d)))

  def bp(self, output, scratch, y, data):
    self.tnn_bp(self.lin_bp(self.softmax_bp((output, scratch), y)), data)

  def update_weights(self):
    for i in xrange(len(self.W)):
      self.W[i][2] = self.momentum * self.W[i][2] + (1 - self.momentum) * self.W[i][1]
      if i == (len(self.W) - 2):
        self.W[i][0] = self.W[i][0] - 100 * self.lr * self.W[i][2] 
      else:
        self.W[i][0] = self.W[i][0] - self.lr * self.W[i][2] 

  def gc(self):
    all_data = [None, (0, None), (4, None, None), \
                (4, (1, None), None), \
                (3, (4, None, None), (0, (3, None, None))), \
                (3, (1, (3, None, None)), (0, (1, (4, (2, None), (3, None, None)))))]
    shape = [w[0].shape for w in self.W]
    eps = 1e-6
    Worg = [copy.copy(w[0].reshape(np.prod(w[0].shape))) for w in self.W]
    y = 5
    for data in all_data:
      (output, scratch), pred = self.fp(data)
      self.clear_dW()
      self.bp(output, scratch, y, data)
      print "Verifing gradient for data:", data
      for j in xrange(len(self.W)):
        print "Over symbol %d" % j
        dW_numeric = np.zeros_like(Worg[j])
        for i in xrange(Worg[j].shape[0]):
          self.W[j][0] = copy.copy(Worg[j])
          self.W[j][0][i] += eps
          self.W[j][0] = self.W[j][0].reshape(shape[j])
          (output0, scratch0), pred0 = self.fp(data)

          self.W[j][0] = copy.copy(Worg[j])
          self.W[j][0][i] -= eps
          self.W[j][0] = self.W[j][0].reshape(shape[j])
          (output1, scratch1), pred1 = self.fp(data)
          dW_numeric[i] = (-np.log(output0[y]) - -np.log(output1[y])) / (2 * eps)
        assert_close(dW_numeric, self.W[j][1])

  def clear_dW(self):
    for i in xrange(len(self.W)):
      self.W[i][1][:] = 0
      self.W[i][2][:] = 0

  def test(self, test_data):
    score = 0
    size = 0
    for y in xrange(len(test_data)):
      for data in test_data[y]:
        _, pred = self.fp(data)
        score += pred == y
        size += 1
    if size == 0:
      return -1
    test_acc = float(score) / float(size)
    print "test acc = %f = %d / %d" % (test_acc, score, size)
    self.scores.append((score, size))
    f = open("scores%d.pkl" % self.seed, 'wb')
    cPickle.dump(self.scores, f)
    self.clear_dW()
    # XXX
    #self.save()

  def save(self):
    print "Saving weights."
    f = open(self.fname, 'wb')
    cPickle.dump(self.W, f)

  def load(self):
    if os.path.isfile(self.fname):
      print "Loading weights %s" % self.fname
      f = open(self.fname, 'r')
      self.W = cPickle.load(f)
    else:
      print "Failed to load %s" % self.fname

  def train(self):

    for depth in [1, 2, 3, 4, 5, 6]:
      train_data, test_data = self.init(depth)
    exit(0)

    for depth in [1, 2, 3, 4, 5, 6]:
      train_data, test_data = self.init(depth)
      if len(train_data) == 0:
        continue
      self.reset_target_matrix(train_data)
      idx = [0] * len(train_data)
      print "_" * 100
      print "Training with %d classes on depth = %d" % (len(train_data), depth)
      train_acc = 0
      epoch = 0
      while train_acc < 0.99:
        score = 0
        for y in xrange(len(train_data)):
          data = train_data[y][idx[y]]
          (output, scratch), pred = self.fp(data)
          score += pred == y
          self.clear_dW()
          self.bp(output, scratch, y, data)
          self.update_weights()
          idx[y] = (idx[y] + 1) % len(train_data[y])
        train_acc = float(score) / len(train_data)
        epoch += 1
        print "epoch = %d, lr = %f, depth = %d, training acc = %f" % (epoch, self.lr, depth, train_acc)
        if epoch % 50 == 0:
          self.test(test_data)
      self.test(test_data)

def main():
  if GC:
    tnn = TNN()
    tnn.gc()
  else:
    for i in range(1):
      pid = os.fork()
      if not pid:
        fname = "tnn_trained/tnn_weights_trained%d.pkl" % i
        tnn = TNN(fname, i)
        tnn.train()
        #os.rename(fname, "tnn_weights_trained%d.pkl" % i)
        exit(0)

if __name__ == '__main__':
  main()

