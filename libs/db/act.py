import os
from .common import *
from .base_db import base_db
from datetime import datetime

class act(base_db):
  def __init__(self, db_dir='', log=None, debug=False):
    ''' Initialize
    '''
    super().__init__(db_dir=db_dir, db_name=ACT_DB, log=log, debug=debug)
    if not self.table_exists(ACT_ACC_TBL):
      self.create_table(ACT_ACC_TBL, ACT_ACC_TBL_SCHEMA, ACT_ACC_TBL_KEY)
    if not self.table_exists(ACT_FAV_TBL):
      self.create_table(ACT_FAV_TBL, ACT_FAV_TBL_SCHEMA, ACT_FAV_TBL_KEY)

  def create_act_tbl(self, act):
    if not self.table_exists(self.format_act_tbl_name(act)):
      self.create_table(self.format_act_tbl_name(act), ACT_TBL_SCHEMA, ACT_TBL_KEY)
            
    ##################
    ##  add/del entries
    ##################

  
  def add_act_pf(self, act, pn, loc):
   # add pf to act table
   self.create_act_tbl(act)
   self.add_row(table_name=self.format_act_tbl_name(act), table_row={COL_PN: pn, COL_LOC: loc})
   self.add_row(table_name=ACT_ACC_TBL, table_row={COL_ACT: act, COL_LAST: datetime.now().strftime(TIMEFORMAT), COL_COUNT: 0, COL_FAV: "N", COL_PIC_FLD: ""})

  def del_act_pf(self, act, pn, loc):
    # 1. delete pf from act table
    self.delete_row(table_name=self.format_act_tbl_name(act),prm={COL_PN: pn, COL_LOC: loc})
    # delete table if no exists
    if self.total_row_count(table_name=self.format_act_tbl_name(act)) == 0:
      self.delete_table(table_name=self.format_act_tbl_name(act))
    # 2. delete pf from fav table
    self.delete_row(table_name=ACT_FAV_TBL, prm={COL_ACT: act})


  def add_act_fav(self, act):
    # 1. add act to favorite table
    self.add_row(table_name=ACT_FAV_TBL, table_row={COL_ACT: act})
    # 2. mark favorite column in access table
    self.update_col(table_name=ACT_ACC_TBL, col={COL_FAV: "Y"}, prm={COL_ACT: act})

  def del_act_fav(self, act):
    # 1. delete act to favorite table
    self.delete_row(table_name=ACT_FAV_TBL, prm={COL_ACT: act})
    # 2. mark unfavorite column in access table
    self.update_col(table_name=ACT_ACC_TBL, col={COL_FAV: "N"}, prm={COL_ACT: act})


  def touch_act(self, act):
    # 1. update last column from main table
    self.update_col(table_name=ACT_ACC_TBL, col={COL_LAST: datetime.now().strftime(TIMEFORMAT)}, prm={COL_ACT: act})
    # 2. Add counter for count column from main table
    self.inc_sngl_col_from_sngl_row(table_name=ACT_ACC_TBL, col=COL_COUNT, prm = {COL_ACT: act})


  def format_act_tbl_name(self, act):
    return act + ACT_TBL