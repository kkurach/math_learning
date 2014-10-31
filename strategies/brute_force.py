from manage.scheduler import Scheduler

class BruteForceScheduler(Scheduler):

  def __init__(self, params):
    Scheduler.__init__(self, params)

  def __str__(self):
    return self.__class__.__name__
  
  def GetEval(self, rule, expr1, expr2):
    return 1
