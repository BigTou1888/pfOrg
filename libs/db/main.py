import os
from .common import *
from .base_db import base_db
from datetime import datetime

class main(base_db):
  def __init__(self, db_dir='', log=None, debug=False):
    ''' Initialize
    '''
    super().__init__(db_dir=db_dir, db_name=MAIN_DB, log=log, debug=debug)

    # initialize the table if not exists
    if not self.table_exists(JP_TBL):
      self.create_table(JP_TBL, JP_TBL_SCHEMA, JP_TBL_KEY)
    if not self.table_exists(MAIN_FAV_TBL):
      self.create_table(MAIN_FAV_TBL, MAIN_FAV_TBL_SCHEMA, MAIN_FAV_TBL_KEY)
    if not self.table_exists(UNKN_TBL):
      self.create_table(UNKN_TBL, UNKN_TBL_SCHEMA, UNKN_TBL_KEY)
    if not self.table_exists(CN_TBL):
      self.create_table(CN_TBL, CN_TBL_SCHEMA, CN_TBL_KEY)

  def add_jp_pf(self, pn, loc, name='', filelist=[], actress=[], gen=[], time='', dur='', company=''):
    ''' add japanese pf to table as a new row, if exists, ignore
      Arguments
      ---------
        pn - p number
        loc - location
        name - pf name
        filelist - file list
        actress - actress list
        gen - genre list
        time - release time
        dur - file duration
        company - produce company
      Returns 
      ---------
        success
    '''
    if not self.row_exists(table_name=JP_TBL, prm={COL_PN: pn, COL_LOC: loc}):
      # add pf to jp table
      table_row = {}
      table_row[COL_PN] = pn
      table_row[COL_LOC] = loc
      table_row[COL_NAME] = name
      table_row[COL_FL]   = filelist
      table_row[COL_ACT]   = actress
      table_row[COL_GEN]   = gen
      table_row[COL_TIME]   = time
      table_row[COL_DUR]   = dur
      table_row[COL_COMPANY]   = company
      table_row[COL_LAST]   = datetime.now().strftime(TIMEFORMAT)
      table_row[COL_COUNT]   = 0
      table_row[COL_FAV]   = "N"
      table_row[COL_PIC_FLD]   = ""
  
      self.add_row(table_name=JP_TBL, table_row=table_row)

  def del_jp_pf (self, pn, loc=''):
    prm = {}
    prm[COL_PN] = pn
    prm[COL_LOC] = loc

    # 1. delete pf from jp table
    self.delete_row(table_name=JP_TBL, prm=prm)
    # 2. delete pf fropm favorite table, if exists
    self.delete_row(table_name=MAIN_FAV_TBL, prm=prm)

  def jp_pf_exists (self, pn, loc=''):
    return self.row_exists(table_name=JP_TBL, prm={COL_PN: pn, COL_LOC: loc})

  def add_jp_fav (self, pn, loc=''):
    # 1. add pf to favorite table
    self.add_row(table_name=MAIN_FAV_TBL, table_row={COL_PN: pn, COL_LOC: loc, COL_PTYPE: "JP"})
    # 2. mark favorite column in jp table
    self.update_col(table_name=JP_TBL, col={COL_FAV: "Y"}, prm={COL_PN: pn, COL_LOC: loc})

  def del_jp_fav (self, pn, loc=''):
    # 1. delete pf from favorite table
    self.delete_row(table_name=MAIN_FAV_TBL, prm={COL_PN: pn, COL_LOC: loc, COL_PTYPE: "JP"})
    # 2. unmark favorite column in jp table
    self.update_col(table_name=JP_TBL, col={COL_FAV: "N"}, prm={COL_PN: pn, COL_LOC: loc})

  def touch_jp(self, pn, loc=''):
    # 1. update last column from main table
    self.update_col(table_name=JP_TBL, col={COL_LAST: datetime.now().strftime(TIMEFORMAT)}, prm={COL_PN: pn, COL_LOC: loc})
    # 2. Add counter for count column from main table
    self.inc_sngl_col_from_sngl_row(table_name=JP_TBL, col=COL_COUNT, prm = {COL_PN: pn, COL_LOC: loc})


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
    self.update_col(table_name=JP_TBL, col={COL_NAME: name}, prm={COL_PN: pn, COL_LOC: loc})

  def get_jp_name (self, pn, loc):
    return self.get_sngl_col_from_sngl_row(table_name=JP_TBL, col=COL_NAME, prm={COL_PN: pn, COL_LOC: loc})


  def add_jp_fl (self, pn, loc, fl=[]):
    self.add_to_col_from_sngl_row(table_name=JP_TBL, col={COL_FL: fl}, prm={COL_PN: pn, COL_LOC: loc} )

  def del_jp_fl (self, pn, loc, fl=[]):
    self.del_from_col(table_name=JP_TBL, col={COL_FL: fl}, prm={COL_PN: pn, COL_LOC: loc} )

  def get_jp_fl (self, pn, loc):
    return self.string2list(self.get_sngl_col_from_sngl_row(table_name=JP_TBL, col=COL_FL, prm={COL_PN: pn, COL_LOC: loc}))

  def add_jp_act (self, pn, loc, act=[]):
    '''
      add actress to exist jp
    '''
    self.add_to_col_from_sngl_row(table_name=JP_TBL, col={COL_ACT: act}, prm={COL_PN: pn, COL_LOC: loc} )

  def del_jp_act (self, pn, loc, act=[]):
    '''
      add actress from exist jp
    '''
    self.del_from_col(table_name=JP_TBL, col={COL_ACT: act}, prm={COL_PN: pn, COL_LOC: loc} )

  def get_jp_act (self, pn, loc):
    return self.string2list(self.get_sngl_col_from_sngl_row(table_name=JP_TBL, col=COL_ACT, prm={COL_PN: pn, COL_LOC: loc}))

  def add_jp_gen (self, pn, loc, gen=[]):
    self.add_to_col_from_sngl_row(table_name=JP_TBL, col={COL_GEN: gen}, prm={COL_PN: pn, COL_LOC: loc} )

  def del_jp_gen (self, pn, loc, gen=[]):
    self.del_from_col(table_name=JP_TBL, col={COL_GEN: gen}, prm={COL_PN: pn, COL_LOC: loc} )

  def get_jp_gen (self, pn, loc):
    return self.string2list(self.get_sngl_col_from_sngl_row(table_name=JP_TBL, col=COL_GEN, prm={COL_PN: pn, COL_LOC: loc}))

  def mod_jp_dur(self, pn, loc, dur):
    self.update_col(table_name=JP_TBL, col={COL_DUR: dur}, prm={COL_PN: pn, COL_LOC: loc})

  def get_jp_dur (self, pn, loc):
    return self.get_sngl_col_from_sngl_row(table_name=JP_TBL, col=COL_DUR, prm={COL_PN: pn, COL_LOC: loc})

  def mod_jp_company(self, pn, loc, company):
    self.update_col(table_name=JP_TBL, col={COL_COMPANY: company}, prm={COL_PN: pn, COL_LOC: loc})

  def get_jp_company(self, pn, loc):
    return self.get_sngl_col_from_sngl_row(table_name=JP_TBL, col=COL_COMPANY, prm={COL_PN: pn, COL_LOC: loc})

  def mod_cn_name (self, loc, name):
    pass

  def add_cn_gen (self, loc, gen=[]):
    pass

  def del_cn_gen (self, loc, gen=[]):
    pass
