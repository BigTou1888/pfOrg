from .main import main
from .act import act
from .gen import gen
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
    self.act_db = act(db_dir=db_dir, log=self.log, debug=debug)
    self.gen_db = gen(db_dir=db_dir, log=self.log, debug=debug)

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
    if not self.main_db.jp_pf_exists(pn=pn, loc=loc):
      # add to main_db.japanese
      self.main_db.add_jp_pf(pn=pn, loc=loc, name=name, filelist=filelist, actress=actress, gen=gen, time=time, dur=dur, company=company)

      # update act_db
      for a in actress:
        self.act_db.add_act_pf(act=a, pn=pn, loc=loc)
      
      # update gen_db
      for g in gen:
        self.gen_db.add_act_pf(gen=g, pn=pn, loc=loc)

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
    actress = self.main_db.get_jp_act(pn=pn, loc=loc)
    gen = self.main_db.get_jp_gen(pn=pn, loc=loc)
    # add to main_db.japanese
    self.main_db.del_jp_pf(pn=pn, loc=loc)

    # update act_db
    for a in actress:
      self.act_db.del_act_pf(act=a, pn=pn, loc=loc)
      
    # update gen_db
    for g in gen:
      self.gen_db.del_gen_pf(gen=g, pn=pn, loc=loc)


  def add_jpf_act(self, pn, loc, actress):
    # 1. add act to jp_table
    self.main_db.add_jp_act(pn, loc, actress)
    # 2. add act to act_table
    if isinstance(actress, list):
      for a in actress:
        self.act_db.add_act_pf(act=a, pn=pn, loc=loc)
    elif isinstance(actress, str):
      self.act_db.add_act_pf(act=actress, pn=pn, loc=loc)
    else:
      self.log.error("type {} not support".format(type(actress)))
    

  def del_jpf_act(self, pn, loc, actress=[]):
    # 1. delete act from jp_table
    self.main_db.del_jp_act(pn, loc, actress)
    # 2. delete act from act_table
    if isinstance(actress, list):
      for a in actress:
        self.act_db.del_act_pf(act=a, pn=pn, loc=loc)
    elif isinstance(actress, str):
      self.act_db.del_act_pf(act=actress, pn=pn, loc=loc)
    else:
      self.log.error("type {} not support".format(type(actress)))

  def add_jpf_gen(self, pn, loc, gen):
    # 1. add gen to jp_table
    self.main_db.add_jp_gen(pn, loc, gen)
    # 2. add gen to gen_table
    if isinstance(gen, list):
      for g in gen:
        self.gen_db.add_gen_pf(gen=g, pn=pn, loc=loc)
    elif isinstance(gen, str):
      self.gen_db.add_gen_pf(gen=gen, pn=pn, loc=loc)
    else:
      self.log.error("type {} not support".format(type(gen)))

  def del_jpf_gen(self, pn, loc, gen):
    # 1. delete gen from jp_table
    self.main_db.del_jp_gen(pn, loc, gen)
    # 2. delete gen from gen_table
    if isinstance(gen, list):
      for g in gen:
        self.gen_db.del_gen_pf(gen=g, pn=pn, loc=loc)
    elif isinstance(gen, str):
      self.gen_db.del_gen_pf(gen=gen, pn=pn, loc=loc)
    else:
      self.log.error("type {} not support".format(type(gen)))
