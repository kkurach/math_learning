#!/usr/bin/python
import sys
import manage.config
from strategies.brute_force import BruteForceScheduler
from strategies.ngram import NgramScheduler
from strategies.tnn_strategy import TNNScheduler
from targets.sum_AAT import SumAAT
from targets.sum_AB import SumAB
from targets.sum_AmultA import SumAmultA
from targets.rbm import RBM
from targets.rbm_sparse import RBMSparse
from targets.sym import Sym
from targets.rbm_oneside import RBMOneSide
from expr.expr_zp import ExprZp
import numpy as np
import time
import signal
import os.path
import copy
from manage.config import APPLIED_RULES, READABLE_RULES, MATLAB

def transfer(scheduler, params, targets, maxpower=5):
  manage.config.NUM_EVAL = manage.config.NUM_HASH
  manage.config.EXPR_IMPL = ExprZp
  trials = 10
  sched = None
  for i in xrange(trials):
    scores = -1 * np.ones((2, maxpower), dtype=np.int32)
    times = -1 * np.ones_like(scores)
    sched = scheduler(params)
    solution_tree = None
    fname = 'results/transfer/%s_%s_%d.txt' % (
        str(sched), targets[0].__name__, i)
    if os.path.isfile(fname):
      continue
    for t in xrange(len(targets)):
      for k in range(1, scores.shape[1]):
        start = time.time()
        target = targets[t](k)
        try:
          signal.signal(signal.SIGALRM, handler)
          signal.alarm(60 * 10)
          sched.Reset()
          sched.SetTarget(target)
          sched.Train(solution_tree)
          sched.Run()
          solution_tree = sched.solution[2]
          scores[t, k] = sched.score
          times[t, k] = (int)(time.time() - start)
        except OSError, exc:
          print "Exception", exc
        print ("Transfering knowledge with schedule %s with"
               "params %s on the targets %s" % (
                    scheduler.__name__, str(params), str(target)))
        print "scores=", scores
        print "times=", times
    record(fname, scores, times)

def execute_once(run_id, scheduler, params, target, maxpower):
  scores = -1 * np.ones((maxpower), dtype=np.int32)
  times = -1 * np.ones_like(scores)
  params['run_id'] = run_id
  sched = scheduler(params)
  solution_tree = None
  comps = {'matlab': [], 'trees': []} 
  fname = 'results/single/%s_%s_%d.txt' % (str(sched), target.__name__, run_id)
  comp_fnames = {}
  comp_fnames['trees'] = 'results/trees/%s_%s.tree' % (str(sched), target.__name__)
  comp_fnames['matlab'] = 'results/matlab/%s_%s.m' % (str(sched), target.__name__)
  if os.path.isfile(fname):
    print "File %s exists." % fname 
    return
  print "Working to produce file %s." % fname

  for k in range(1, scores.shape[0]):
    t = target(k)
    sched.Reset()
    sched.SetTarget(t)
    sched.Train(solution_tree)
    start = time.time()
    try:
      signal.signal(signal.SIGALRM, handler)
      signal.alarm(60 * 10)
      sched.Run()
      solution_tree = [s[APPLIED_RULES] for s in sched.solution[1]]
      comps['trees'].append([s[READABLE_RULES] for s in sched.solution[1]])
      comps['matlab'].append([(w, s[MATLAB]) for (w, s) in zip(sched.solution[0], sched.solution[1])])
      print "\nApplied rules:"
      print solution_tree
      scores[k] = sched.score
      times[k] = (int)(time.time() - start)
    except OSError, exc:
      print "Exception", exc
    print "Executing schedule %s with params %s on the target %s" % \
      (str(sched), str(params), str(t))
    print "scores=", scores
    print "times=", times
    signal.alarm(0)
 
  record(fname, scores, times)
  for name in ['matlab', 'trees']:
    comp = comps[name]
    comp_fname = comp_fnames[name]
    with open(comp_fname, 'w') as f:
      for c in comp:
        if name == 'trees':
          for i, t in enumerate(c):
            if i > 0:
              f.write('@@@@@')
            f.write(str(t))
        else:
          for i, (w, t) in enumerate(c):
            f.write(str(w) + " * " + str(t))
            if i < len(c) - 1:
              f.write(" + ")
        f.write('\n')

def execute(scheduler, params, target, maxpower=12):
  manage.config.NUM_EVAL = manage.config.NUM_HASH
  manage.config.EXPR_IMPL = ExprZp
  trials = params['trials']
  for i in xrange(trials):
    execute_once(i, scheduler, params, target, maxpower)

def handler(*_):
  print "Forever is over!"
  raise OSError("end of time")

def record(fname, scores, times):
  with open(fname, 'w') as f:
    f.write("scores=" + str(scores))
    f.write("\n")
    f.write("times=" + str(times))

def main():
  schedulers = {'brute_force': BruteForceScheduler,
                'ngram': NgramScheduler,
                'tnn': TNNScheduler}
  targets = {'sum_AAT': SumAAT,
             'sum_AB': SumAB,
             'sum_AmultA': SumAmultA,
             'rbm': RBM,
             'rbm_oneside': RBMOneSide,
             'sym': Sym}
  scheduler = "ngram"
  target = "sum_AB"
  params = {'depth': 5, 'trials': 1}
  if len(sys.argv) > 1:
    scheduler = sys.argv[1]
  if len(sys.argv) > 2:
    targets = sys.argv[2]
  assert scheduler in schedulers
  assert target in targets
  scheduler = schedulers[scheduler]
  target = targets[target]
  execute(scheduler, params, target, maxpower=15)

if __name__ == '__main__':
  main()
