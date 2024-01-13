TIMEFORMAT  = "%Y-%m-%d_%H-%M-%S"

LIST_SEP    = ',-| '
COL_PN      = 'pn'
COL_LOC     = 'location'
COL_NAME    = 'name'
COL_FL      = 'filelist'
COL_ACT     = 'actress'
COL_GEN     = 'genre'
COL_TIME    = 'time'
COL_DUR     = 'duration'
COL_COMPANY = 'company'
COL_WAIT    = 'downloading'
COL_LAST    = 'last_time_watch'
COL_COUNT   = 'watch_times'
COL_FAV     = 'favorite'
COL_PIC_FLD = 'pic_folder'

COL_PTYPE = 'ptype'

# main database
# main table
MAIN_DB = "main"
JP_TBL = 'japanese_table'
JP_TBL_SCHEMA = [[COL_PN,       'TEXT', 'NOT NULL'], 
                     [COL_LOC,      'TEXT', 'NOT NULL'], 
                     [COL_NAME,     'TEXT', 'NOT NULL'], 
                     [COL_FL,       'TEXT', 'NOT NULL'], 
                     [COL_ACT,      'TEXT', 'NOT NULL'], 
                     [COL_GEN,      'TEXT', 'NOT NULL'], 
                     [COL_TIME,     'TEXT', 'NOT NULL'], 
                     [COL_DUR,      'TEXT', 'NOT NULL'], 
                     [COL_COMPANY,  'TEXT', 'NOT NULL'],
                     [COL_LAST,     'TEXT', 'NOT NULL'],
                     [COL_COUNT,    'TEXT', 'NOT NULL'],
                     [COL_FAV,      'TEXT', 'NOT NULL'],
                     [COL_PIC_FLD,      'TEXT', 'NOT NULL']
                     ]
JP_TBL_KEY = [COL_PN, COL_LOC]

# chinese table
CN_TBL = 'chinese_table'
CN_TBL_SCHEMA = [ [COL_LOC, 'TEXT', 'NOT NULL'], 
                  [COL_NAME, 'TEXT', 'NOT NULL'],
                  [COL_FL,       'TEXT', 'NOT NULL'], 
                  [COL_GEN,      'TEXT', 'NOT NULL'], 
                  [COL_LAST,     'TEXT', 'NOT NULL'],
                  [COL_COUNT,    'TEXT', 'NOT NULL'],
                  [COL_FAV,      'TEXT', 'NOT NULL'] ]
CN_TBL_KEY = [COL_LOC]

# unknown table
UNKN_TBL = 'unknown_table'
UNKN_TBL_SCHEMA = [[COL_LOC, 'TEXT', 'NOT NULL'], 
                  [COL_NAME, 'TEXT', 'NOT NULL'],
                  [COL_FL,       'TEXT', 'NOT NULL'], 
                  [COL_GEN,      'TEXT', 'NOT NULL'], 
                  [COL_LAST,     'TEXT', 'NOT NULL'],
                  [COL_COUNT,    'TEXT', 'NOT NULL'],
                  [COL_FAV,      'TEXT', 'NOT NULL'] ]

UNKN_TBL_KEY = [COL_LOC]

# favorite table
MAIN_FAV_TBL = 'favorite_table'
MAIN_FAV_TBL_SCHEMA = [  
                       [COL_PN,      'TEXT', 'NOT NULL'],
                       [COL_LOC,      'TEXT', 'NOT NULL'],
                       [COL_PTYPE,     'TEXT', 'NOT NULL']
                   ]
MAIN_FAV_TBL_KEY = [ COL_LOC]



# actress database
ACT_DB = "act"
ACT_TBL = '_table'
COL_ACT     = 'actress'
ACT_TBL_SCHEMA = [  [COL_PN,    'TEXT', 'NOT NULL'], 
                      [COL_LOC,   'TEXT', 'NOT NULL']
                     ]
ACT_TBL_KEY = [COL_PN, COL_LOC]

ACT_ACC_TBL = 'access_table'
ACT_ACC_TBL_SCHEMA = [  [COL_ACT,    'TEXT', 'NOT NULL'], 
                      [COL_LAST,  'TEXT', 'NOT NULL'],
                      [COL_COUNT, 'TEXT', 'NOT NULL'],
                      [COL_FAV,   'TEXT', 'NOT NULL'],
                      [COL_PIC_FLD,      'TEXT', 'NOT NULL']
                     ]
ACT_ACC_TBL_KEY = [COL_ACT]

ACT_FAV_TBL = 'favorite_table'
ACT_FAV_TBL_SCHEMA = [  [COL_ACT,    'TEXT', 'NOT NULL'] ]
ACT_FAV_TBL_KEY = [COL_ACT]


# genre database
GEN_DB = "gen"
GEN_TBL = '_table'
GEN_TBL_SCHEMA = [  [COL_PN,    'TEXT', 'NOT NULL'], 
                      [COL_LOC,   'TEXT', 'NOT NULL'],
                      [COL_NAME,  'TEXT', 'NOT NULL']
                     ]
GEN_TBL_KEY = [COL_PN, COL_LOC]

GEN_ACC_TBL = 'access_table'
GEN_ACC_TBL_SCHEMA = [  [COL_GEN,    'TEXT', 'NOT NULL'], 
                      [COL_LAST,  'TEXT', 'NOT NULL'],
                      [COL_COUNT, 'TEXT', 'NOT NULL'],
                      [COL_FAV,   'TEXT', 'NOT NULL']
                     ]
GEN_ACC_TBL_KEY = [COL_GEN]

GEN_FAV_TBL = 'favorite_table'
GEN_FAV_TBL_SCHEMA = [  [COL_GEN,    'TEXT', 'NOT NULL'] ]
GEN_FAV_TBL_KEY = [COL_GEN]