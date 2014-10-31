from manage.scheduler import Scheduler
import heapq
from manage.mock_cache import MockCache

class TrainingScheduler(Scheduler):

  def __init__(self, params):
    Scheduler.__init__(self, params)

  def Reset(self):
    super(TrainingScheduler, self).Reset()
    self.cache = MockCache()

  def __str__(self):
    return self.__class__.__name__
  
  def GetEval(self, rule, expr1, expr2):
    return 1

  def Run(self):
    while len(self.pq) > 0:
      score, best_elem = heapq.heappop(self.pq)
      rule, expr1, expr2 = best_elem
      self.Apply(rule, expr1, expr2)

    assert False, "No new expression before FoundTarget"
