import os
from .common import *
from .base_db import base_db

class act(base_db):
    def __init__(self, cfg, log=None, db_dir='', debug=False, test=False):
        super().__init__(log=log, dbDir=db_dir, dbName=ACT_DB, initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=False, cacheEntries=False)

        for act in cfg:
          if not self.tableExists(act+ACT_TBL):
            self.createTable(act+ACT_TBL, ACT_TBL_SCHEMA, ACT_TBL_KEY)
            
    ##################
    ##  add/del entries
    ##################

  
    def add_act_pf(self, act, pn, loc, name=''):
      # add pf to act table
      pass

    def del_act_pf(self, act, pn, loc):
      # add pf to act table
      pass

    def add_act_fav(self, act):
      # add actress to favorite table
      pass

    def del_act_fav(self, act):
      # delete actress from favorite table
      pass


    def touch_act(self, act):
       # update access table
       pass

