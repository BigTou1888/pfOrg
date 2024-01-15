import os
from .common import *
from .base_db import base_db
from datetime import datetime

class gen(base_db):
  def __init__(self, db_dir='', log=None, debug=False):
    ''' Initialize
    '''
    super().__init__(db_dir=db_dir, db_name=GEN_DB, log=log, debug=debug)
    if not self.table_exists(GEN_ACC_TBL):
      self.create_table(GEN_ACC_TBL, GEN_ACC_TBL_SCHEMA, GEN_ACC_TBL_KEY)
    if not self.table_exists(GEN_FAV_TBL):
      self.create_table(GEN_FAV_TBL, GEN_FAV_TBL_SCHEMA, GEN_FAV_TBL_KEY)

  def create_gen_tbl(self, gen):
    if not self.table_exists(self.format_gen_tbl_name(gen)):
      self.create_table(self.format_gen_tbl_name(gen), GEN_TBL_SCHEMA, GEN_TBL_KEY)
            
    ##################
    ##  add/del entries
    ##################

  
  def add_gen_pf(self, gen, pn, loc):
   # add pf to gen table
   self.create_gen_tbl(gen)
   self.add_row(table_name=self.format_gen_tbl_name(gen), table_row={COL_PN: pn, COL_LOC: loc})
   self.add_row(table_name=GEN_ACC_TBL, table_row={COL_GEN: gen, COL_LAST: datetime.now().strftime(TIMEFORMAT), COL_COUNT: 0, COL_FAV: "N"})

  def del_gen_pf(self, gen, pn, loc):
    # 1. delete pf from gen table
    self.delete_row(table_name=self.format_gen_tbl_name(gen),prm={COL_PN: pn, COL_LOC: loc})
    if self.total_row_count(table_name=self.format_gen_tbl_name(gen)) == 0:
      self.delete_table(table_name=self.format_gen_tbl_name(gen))
    # 2. delete pf from fav table
    self.delete_row(table_name=GEN_FAV_TBL, prm={COL_GEN: gen})

  def add_gen_fav(self, gen):
    # 1. add gen to favorite table
    self.add_row(table_name=GEN_FAV_TBL, table_row={COL_GEN: gen})
    # 2. mark favorite column in access table
    self.update_col(table_name=GEN_ACC_TBL, col={COL_FAV: "Y"}, prm={COL_GEN: gen})

  def del_gen_fav(self, gen):
    # 1. delete gen to favorite table
    self.delete_row(table_name=GEN_FAV_TBL, prm={COL_GEN: gen})
    # 2. mark unfavorite column in access table
    self.update_col(table_name=GEN_ACC_TBL, col={COL_FAV: "N"}, prm={COL_GEN: gen})


  def touch_gen(self, gen):
    # 1. update last column from main table
    self.update_col(table_name=GEN_ACC_TBL, col={COL_LAST: datetime.now().strftime(TIMEFORMAT)}, prm={COL_GEN: gen})
    # 2. Add counter for count column from main table
    self.inc_sngl_col_from_sngl_row(table_name=GEN_ACC_TBL, col=COL_COUNT, prm = {COL_GEN: gen})


  def format_gen_tbl_name(self, gen):
    return gen + GEN_TBL
