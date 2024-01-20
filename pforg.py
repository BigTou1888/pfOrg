import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

import db.db_mngt
import dir.jp
from log.log import log
from http_server.server import http_server

LOG_DIR = 'log'
DB_DIR = 'dbs'

DEBUG = True
TEST = False

# instantiate log
app_log = log(log_dir=LOG_DIR, log_name='pforg_log', debug=DEBUG)

# instantiate db_mngt
db_mngt = db.db_mngt.db_mngt('./dbs', app_log, DEBUG)



db_mngt.add_jp_pf("", "/home/user/MUM-123")
db_mngt.add_jp_pf("MUM-123", "")
db_mngt.add_jp_pf("MUM-123", "/home/user/MUM-123")
db_mngt.add_jp_pf(pn="MUM-456", 
                  loc="/home/user/MUM-456", 
                  name="mum-456 test", 
                  filelist=["/home/user/MUM-456/p1.jpg", "/home/user/MUM-456/p2.jpg", "/home/user/MUM-456/p2.mpeg"], 
                  actress=["范晓萱", "张韶涵"])
db_mngt.add_jp_pf(pn="MUM-456", 
                  loc="/home/user/MUM-456", 
                  name="mum-456 test", 
                  filelist=["/home/user/MUM-456/p1.jpg", "/home/user/MUM-456/p2.jpg", "/home/user/MUM-456/p2.mpeg"], 
                  actress=["范晓萱", "张韶涵", "张含韵"])
db_mngt.add_jp_pf(pn="MUM-456", 
                  loc="/home/user/MUM-456_dup", 
                  name="mum-456 test", 
                  filelist=["/home/user/MUM-456/p1.jpg", "/home/user/MUM-456/p2.jpg", "/home/user/MUM-456/p2.mpeg"], 
                  actress=["范晓萱", "张韶涵", "张含韵"])


db_mngt.add_jpf_act(pn="MUM-456", loc="/home/user/MUM-456_dup", actress=["张含韵", "关晓彤"])
db_mngt.add_jpf_act(pn="MUM-456", loc="/home/user/MUM-456_dup", actress=["张含韵", "关晓彤"])
db_mngt.add_jpf_act(pn="MUM-456", loc="/home/user/MUM-456", actress=["赵今麦"])
db_mngt.add_jpf_act(pn="MUM-456", loc="/home/user/MUM-456", actress=["赵今麦"])

db_mngt.del_jpf_act(pn="MUM-456", loc="/home/user/MUM-456_dup", actress="范晓萱")
db_mngt.del_jpf_act(pn="MUM-456", loc="/home/user/MUM-456_dup", actress=["张韶涵"])
db_mngt.del_jpf_act(pn="MUM-456", loc="/home/user/MUM-456_dup", actress=["范晓萱","张韶涵"])
db_mngt.del_jpf_act(pn="MUM-456", loc="/home/user/MUM-456", actress=["范晓萱", "张韶涵"])

db_mngt.add_jpf_act("", "/home/user/MUM-123", actress="张子枫")
db_mngt.add_jpf_act("", "/home/user/MUM-123", actress="张子枫")
db_mngt.add_jpf_act("", "/home/user/MUM-123", actress="张子枫")
db_mngt.add_jpf_act("", "/home/user/MUM-123", actress="张子枫")
db_mngt.add_jpf_act("", "/home/user/MUM-123", actress="辛芷蕾")
db_mngt.add_jpf_act("", "/home/user/MUM-123", actress="张子枫")
db_mngt.add_jpf_act("", "/home/user/MUM-123", actress="张子枫")

db_mngt.del_jpf_act("", "/home/user/MUM-123", actress="张子枫")

#print(db_mngt.main_db.get_jp_name("%%", "%%"))
print (db_mngt.main_db.get_jp_name("MUM-456", "/home/user/MUM-456"))
print (db_mngt.main_db.get_jp_act("MUM-456", "/home/user/MUM-456_dup"))

#db_mngt.del_jp_pf("", "/home/user/MUM-123")
# db_mngt.del_jp_pf("MUM-123", "")
db_mngt.main_db.add_jp_fav("MUM-456", "/home/user/MUM-456")
db_mngt.main_db.add_jp_fav("MUM-456", "/home/user/MUM-456_dup")
db_mngt.main_db.del_jp_fav("MUM-456", "/home/user/MUM-456_dup")
db_mngt.main_db.touch_jp("MUM-456", "/home/user/MUM-456_dup")

db_mngt.main_db.total_row_count("japanese_table")
jp = dir.jp.find_jp_movie("F:/名优分类")

http = http_server(debug=DEBUG)
http.run()