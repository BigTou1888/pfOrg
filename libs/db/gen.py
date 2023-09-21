import os
from .common import *
from .base_db import base_db

class gen(base_db):
    def __init__(self, cfg, log=None, db_dir='', debug=False, test=False):

        super().__init__(log=log, dbDir=db_dir, dbName=GEN_DB, initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=False, cacheEntries=False)

        for main_gen in cfg:
          for gen in cfg[main_gen]:
            if not self.tableExists(gen+GEN_TBL):
              self.createTable(gen+GEN_TBL, GEN_TBL_SCHEMA, GEN_TBL_KEY)
            
    ##################
    ##  add/del entries
    ##################

  
    def add_gen_pf(self, gen, pn, loc, name=''):
      # add pf to genre table
      pass

    def del_gen_pf(self, gen, pn, loc):
      # add pf to genre table
      pass

    def add_gen_fav(self, gen):
      # add genre to favorite table
      pass

    def del_gen_fav(self, gen):
      # delete genre from favorite table
      pass


    def touch_gen(self, gen):
       # update access table
       pass

