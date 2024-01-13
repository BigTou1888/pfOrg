from .main import main
from log.log import log as logger

class db_mngt():
  def __init__(self, db_dir='', log=None, debug=False):

    if db_dir == "":
      print("Need to pass database directory")
      exit(0)
    else:
      self.db_dir = db_dir

    if log is None:
      self.log = logger(log_dir='', log_name='db_mngt_log', debug=debug)
    else:
      self.log = log
    
    self.debug = debug
    
    self.main_db = main(db_dir=db_dir, log=self.log, debug=debug)

  def add_jp_pf(self, pn, loc, name='', filelist=[], actress=[], gen=[], time='', dur='', company=''):
    ''' add japanese pf to main_db, and update acctress db, gen db
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
    # add to main_db.japanese
    self.main_db.add_jp_pf(pn=pn, loc=loc, name=name, filelist=filelist, actress=actress, gen=gen, time=time, dur=dur, company=company)

    # update act_db
    for a in actress:
      pass
      
    # update gen_db
    for g in gen:
      pass

  def del_jp_pf(self, pn, loc):
    ''' delete japanese pf from main_db, and update acctress db gen db
      Arguments
      ---------
        pn - p number
        loc - location
      Returns 
      ---------
        success
    '''
    # add to main_db.japanese
    self.main_db.del_jp_pf(pn=pn, loc=loc)

    # update act_db
    #for a in actress:
      #pass
      
    # update gen_db
    #for g in gen:
      #pass



  def add_jpf_act(self, pn, loc, actress=[]):
    # 1. add act to jp_table
    self.main_db.add_jp_act(pn, loc, actress)
    # 2. add act to act_table

  def del_jpf_act(self, pn, loc, actress=[]):
    # 1. delete act from jp_table
    self.main_db.del_jp_act(pn, loc, actress)
    # 2. delete act from act_table