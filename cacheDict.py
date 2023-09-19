from collections import OrderedDict
class cacheDict():
  '''
    cached dictationary, 
    cacheLimit = 0: no cache, 
    cacheLimit = -1: unlimitted entries
    cacheLimit > 0: cached item
  '''
  def __init__(self, cacheLimit=0):
    self.cacheLimit = cacheLimit
    # cache, indexed by cmd, value is {'result': '', 'id': ''}
    self.cache = {}
    # order, indexed by id
    # when want to kickoff an item, kick the first one. 
    self.order = OrderedDict()

    self.curId = 0

  def updDict(self, cmd, result):
    # cache is enable
    if self.cacheLimit != 0:
      if cmd in self.cache:
        # delete old order
        prevId = self.cache[cmd]['id']
        del self.order[prevId]
      
      # update new item
      self.cache[cmd] = {'result': result, 'id': self.curId}
      self.order[self.curId] = cmd

      if self.cacheLimit > 0 and len(self.cache) > self.cacheLimit:
        # delete oldest one
        oldestCmd = self.order.popitem(last=False)[1]
        del self.cache[oldestCmd]
      self.curId += 1

  def getResult(self, cmd):
    if cmd in self.cache:
      result = self.cache[cmd]['result']
      self.updDict(cmd, result)
      return (True, result)
    else:
      return (False, None)

