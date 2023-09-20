import os
from .common import *
from .db import base_db

class main(base_db):
    def __init__(self, name='', log=None, dbDir='sql', dbName='pdb', initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=False, cacheEntries=0):
        if dbDir == '':
            self.dbDir = os.getcwd()
        else:
            self.dbDir = dbDir
        super().__init__(name=dbName, log=log, dbDir=self.dbDir, dbName=dbName, initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=selfLock, cacheEntries=cacheEntries)

        # initialize the table if not exists
        if not self.tableExists(MAIN_TABLE):
            self.createTable(MAIN_TABLE, MAIN_TABLE_SCHEMA, MAIN_TABLE_KEY)
        if not self.tableExists(FAV_TABLE):
            self.createTable(FAV_TABLE, FAV_TABLE_SCHEMA, FAV_TABLE_KEY)
        if not self.tableExists(UNKNOWN_TABLE):
            self.createTable(UNKNOWN_TABLE, UNKNOWN_TABLE_SCHEMA, UNKNOWN_TABLE_KEY)
        if not self.tableExists(CHINA_TABLE):
            self.createTable(CHINA_TABLE, CHINA_TABLE_SCHEMA, CHINA_TABLE_KEY)

    ##################
    ##  add/del entries
    ##################

  
    def add_pn(self, pn, loc='', name='', filelist=[], actress=[], gen=[], time='', company=''):
      # add pn to main table
      pass


    def del_pn (self, pn, loc=''):
      # 1. delete pn from main table
      # 2. delete pn fropm favorite table, if exists
      pass

    def add_fav (self, pn, loc=''):
      # 1. add pn to favorite table
      # 2. mark favorite column in main table
      pass

    def del_fav (self, pn, loc=''):
      # 1. delete pn from favorite table
      # 2. unmark favorite column in main table
      pass


    ##################
    ##  modify entries
    ##################


