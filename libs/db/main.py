import os
from .common import *
from .base_db import base_db

class main(base_db):
    def __init__(self, cfg, log=None, db_dir='', debug=False, test=False):
        self.cfg = cfg
        super().__init__(log=log, dbDir=db_dir, dbName=MAIN_DB, initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=False, cacheEntries=False)

        # initialize the table if not exists
        if not self.tableExists(JP_TBL):
            self.createTable(JP_TBL, JP_TBL_SCHEMA, JP_TBL_KEY)
        if not self.tableExists(MAIN_FAV_TBL):
            self.createTable(MAIN_FAV_TBL, MAIN_FAV_TBL_SCHEMA, MAIN_FAV_TBL_KEY)
        if not self.tableExists(UNKN_TBL):
            self.createTable(UNKN_TBL, UNKN_TBL_SCHEMA, UNKN_TBL_KEY)
        if not self.tableExists(CN_TBL):
            self.createTable(CN_TBL, CN_TBL_SCHEMA, CN_TBL_KEY)

    ##################
    ##  add/del/touch entries
    ##################

  
    def add_jp_pf(self, pn, loc, name='', filelist=[], actress=[], gen=[], time='', dur='', company=''):
      # add pf to jp table
      pass


    def del_jp_pf (self, pn, loc=''):
      # 1. delete pf from jp table
      # 2. delete pf fropm favorite table, if exists
      pass

    def add_jp_fav (self, pn, loc=''):
      # 1. add pf to favorite table
      # 2. mark favorite column in jp table
      pass

    def del_jp_fav (self, pn, loc=''):
      # 1. delete pf from favorite table
      # 2. unmark favorite column in jp table
      pass

    def touch_jp(self, pn, loc=''):
      # 1. update pf from main table
      # 2. update pf from fav table if exists
      pass


    def add_cn_pf(self, loc, name='', gen=[]):
      # add pf to cn table
      pass


    def del_cn_pf (self, loc):
      # 1. delete pf from cn table
      # 2. delete pf fropm favorite table, if exists
      pass

    def add_cn_fav (self, loc):
      # 1. add pf to favorite table
      # 2. mark favorite column in cn table
      pass

    def del_cn_fav (self, loc):
      # 1. delete pf from favorite table
      # 2. unmark favorite column in cn table
      pass

    def touch_cn(self, loc=''):
      # 1. update pf from cn table
      # 2. update pf from fav table if exists
      pass


    def add_unkn_pf(self, loc, name='', gen=[]):
      # add pf to unkn table
      pass


    def del_unkn_pf (self, loc):
      # 1. delete pf from unkn table
      # 2. delete pf fropm favorite table, if exists
      pass

    def add_unkn_fav (self, loc):
      # 1. add pf to favorite table
      # 2. mark favorite column in unkn table
      pass

    def del_unkn_fav (self, loc):
      # 1. delete pf from favorite table
      # 2. unmark favorite column in unkn table
      pass

    def touch_unkn(self, loc=''):
      # 1. update pf from unknown table
      # 2. update pf from fav table if exists
      pass



    ##################
    ##  modify entries
    ##################
    def mod_jp_name (self, pn, loc, name):
      pass

    def add_jp_fl (self, pn, loc, fl=[]):
      pass

    def del_jp_fl (self, pn, loc, fl=[]):
      pass

    def add_jp_act (self, pn, loc, act=[]):
      pass

    def del_jp_act (self, pn, loc, act=[]):
      pass

    def add_jp_gen (self, pn, loc, gen=[]):
      pass

    def del_jp_gen (self, pn, loc, gen=[]):
      pass

    def mod_jp_time(self, pn, loc, time):
      pass

    def mod_jp_dur(self, pn, loc, dur):
      pass

    def mod_jp_company(self, pn, loc, company):
      pass

    def mod_cn_name (self, loc, name):
      pass

    def add_cn_gen (self, loc, gen=[]):
      pass

    def del_cn_gen (self, loc, gen=[]):
      pass
