import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

from db.db_mngt import db_mngt
from log.log import log

LOG_DIR = 'log'
DB_DIR = 'dbs'

DEBUG = False
TEST = False

app_log = log(log_dir=LOG_DIR, log_name='pforg_log', debug=DEBUG)

db_mngt = db_mngt(main_cfg={}, act_cfg={}, gen_cfg={}, log=app_log, db_dir=DB_DIR, debug=DEBUG, test=TEST)