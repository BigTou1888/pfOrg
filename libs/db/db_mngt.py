from .main import main
from .act import act
from .gen import gen

class db_mngt():

  def __init__(self, main_cfg, act_cfg, gen_cfg, log=None, db_dir='', debug=False, test=False):
    if log is None:
      print("Need to pass log object")
      exit(0)
    
    if db_dir == "":
      print("Need to pass database directory")
      exit(0)

    self.main_cfg = main_cfg
    self.act_cfg = act_cfg
    self.gen_cfg = gen_cfg 
    self.log = log
    self.db_dir = db_dir
    self.debug = debug
    self.test = test
    self.main_db = main(main_cfg, log, db_dir, debug, test)
    self.act_db = act(act_cfg, log, db_dir, debug, test)
    self.gen_db = gen(gen_cfg, log, db_dir, debug, test)