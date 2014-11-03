#!/usr/bin/python
import sys
import os
sys.path.insert(0, '../')
import numpy as np
import signal
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
from manage.config import MATLAB, APPLIED_RULES

def handler(*_):
  print "Forever is over!"
  raise OSError("end of time")

def execute_once(scheduler, params, target, solution_tree, k):
  t = target(k)
  scheduler.Reset()
  scheduler.SetTarget(t)
  scheduler.Train(solution_tree)
  matlab = None
  try:
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30 * 60)
    scheduler.Run()
    solution_tree = [s[APPLIED_RULES] for s in scheduler.solution[1]]
    matlab = [(w, s[MATLAB]) for (w, s) in zip(scheduler.solution[0], scheduler.solution[1])]
  except OSError, exc:
    print "Exception", exc
    return None, None
  print "Executing schedule %s with params %s on the target %s" % \
    (str(scheduler), str(params), str(t))
  signal.alarm(0)
  return matlab, solution_tree
 

def main():
  targets =  [(SumAAT, "$\mathbf{(\sum AA^T)_k}$"),
             (SumAB, "$\mathbf{(\sum AB)_k}$"),
             (SumAmultA, "$\mathbf{(\sum (A.*A)A^T})_k$"),
             (Sym, "{\\bf Sym$_k$}"),
             (RBMOneSide, "{\\bf (RBM-1)$_k$}"),
             (RBM, "{\\bf (RBM-2)$_k$}")]
  os.remove('sup.tex')
  sup = open('sup.tex', 'w')
  for target, labels in targets:
    sup.write("\n\n\subsection{%s}\n\n" % labels)
    manage.config.EXPR_IMPL = ExprZp
    manage.config.NUM_EVAL = manage.config.NUM_HASH
    params = {'depth': 5, 'trials': 1, 'run_id': 1}
    scheduler = NgramScheduler(params)
    solution_tree = None
    for i in range(1, 16):
      matlab, solution_tree = execute_once(scheduler, params, target, solution_tree, i)
      if matlab is None:
        break
      f = open('code.m', 'w')
      original = target(i).GetTargetExpression()
      code = ""
      code += original.comp[MATLAB] + "\n"
      code += "optimized = "
      expr = ""
      try:
        for w, c in matlab:
          if len(expr) > 0:
            expr += " + "
          expr += "%s * (%s)" % (ExprZp.ToFrac(w), c)
      except:
        continue
      if target == RBM:
        expr = "2^(n + m - %d) * (%s)" % (manage.config.N + manage.config.M, expr)
      if target == RBMOneSide:
        expr = "2^(n - %d) * (%s)" % (manage.config.M, expr)
      code += expr + ";\n"
      code += "normalization = sum(abs(original(:)));\n";
      code += "assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);"
      f.write(code)
      f.close()
      print "Executing matlab code: \n%s\n" % code
      ret = os.system("matlab -nodesktop -nodisplay -nojvm -nosplash -r \"try run('code.m');catch exit(-1); end; exit(0) \" > /dev/null")
      if ret == 0:
        sup.write("\n\n{\\bf k = %d}\n\n" % i)
        sup.write("\\begin{lstlisting}\n")
        sup.write(code)
        sup.write("\n\\end{lstlisting}\n")
        sup.flush()
      else:
        continue
      os.remove('code.m')
  sup.close()

if __name__ == '__main__':
  main()
