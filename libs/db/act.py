import os
from .common import *
from .base_db import base_db

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

  
  def add_act_pf(self, act, pn, loc, name=''):
   # add pf to act table
   self.create_act_tbl(act)
   self.add_row(table_name=self.format_act_tbl_name(act), table_row={COL_PN: pn, COL_LOC: loc})

  def del_act_pf(self, act, pn, loc):
    # add pf to act table
    self.delete_row(table_name=self.format_act_tbl_name(act),prm={COL_PN: pn, COL_LOC: loc})
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


  def format_act_tbl_name(self, act):
    return act + ACT_TBL