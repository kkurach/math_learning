#!/usr/bin/python
import sys
import os
sys.path.insert(0, '../')
import numpy as np
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
from manage.config import MATLAB
from main import execute_once


def main():
  targets = [(SumAAT, "$\mathbf{(\sum AA^T)_k}$"),
             (SumAB, "$\mathbf{(\sum AB)_k}$"),
             (SumAmultA, "$\mathbf{\sum (A.*A)A^T})_k$"),
             (Sym, "{\\bf Sym$_k$}"),
             (RBMOneSide, "{\\bf (RBM-1)$_k$}"),
             (RBM, "{\\bf (RBM-2)$_k$}")]
  os.remove('sup.tex')
  sup = open('sup.tex', 'w')
  for target, labels in targets:
    sup.write("\n\n\subsection{%s}\n\n" % labels)
    manage.config.EXPR_IMPL = ExprZp
    manage.config.NUM_EVAL = manage.config.NUM_HASH
    scheduler = NgramScheduler
    params = {'depth': 5, 'trials': 1}
    matlab = execute_once(1, scheduler, params, target, maxpower=15, record_it=False, until_exception=True)["matlab"]
    for i, m in enumerate(matlab):
      f = open('code.m', 'w')
      original = target(i + 1).GetTargetExpression()
      code = ""
      code += original.comp[MATLAB] + "\n"
      code += "optimized = "
      expr = ""
      for w, c in m:
        if len(expr) > 0:
          expr += " + "
        expr += "%s * (%s)" % (ExprZp.ToFrac(w), c)
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
        sup.write("\n\n{\\bf k = %d}\n\n" % (i + 1))
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
