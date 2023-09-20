COL_PN      = 'pn'
COL_LOC     = 'location'
COL_NAME    = 'name'
COL_FL      = 'filelist'
COL_ACT     = 'actress'
COL_GEN     = 'genre'
COL_TIME    = 'time'
COL_DUR     = 'duration'
COL_COMPANY = 'company'
COL_LAST    = 'last time watch'
COL_COUNT   = 'watch times'
COL_FAV     = 'favorite'

# main database
# main table
MAIN_TABLE = 'main'
MAIN_TABLE_SCHEMA = [[COL_PN,       'TEXT', 'NOT NULL'], 
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
                     [COL_FAV,      'TEXT', 'NOT NULL']
                     ]
MAIN_TABLE_KEY = [COL_PN, COL_LOC]

# favorite table
FAV_TABLE = 'favorite'
FAV_TABLE_SCHEMA = [  [COL_PN,       'TEXT', 'NOT NULL'], 
                      [COL_LOC,      'TEXT', 'NOT NULL'], 
                      [COL_NAME,     'TEXT', 'NOT NULL']
                   ]
FAV_TABLE_KEY = [COL_PN, COL_LOC]

# unknown table
UNKNOWN_TABLE = 'unknown'
UNKNOWN_TABLE_SCHEMA = [[COL_LOC, 'TEXT', 'NOT NULL'], 
                        [COL_NAME, 'TEXT', 'NOT NULL'] ]
UNKNOWN_TABLE_KEY = [COL_LOC]

# chinese table
CHINA_TABLE = 'china'
CHINA_TABLE_SCHEMA = [[COL_LOC, 'TEXT', 'NOT NULL'], 
                      [COL_NAME, 'TEXT', 'NOT NULL'] ]
CHINA_TABLE_KEY = [COL_LOC]



# actress database
ACT_TABLE_SCHEMA = [  [COL_PN,    'TEXT', 'NOT NULL'], 
                      [COL_LOC,   'TEXT', 'NOT NULL'],
                      [COL_NAME,  'TEXT', 'NOT NULL'], 
                      [COL_LAST,  'TEXT', 'NOT NULL'],
                      [COL_COUNT, 'TEXT', 'NOT NULL'],
                      [COL_FAV,   'TEXT', 'NOT NULL']
                     ]
ACT_TABLE_KEY = [COL_PN, COL_LOC]


# genre database
GEN_TABLE_SCHEMA = [  [COL_PN,    'TEXT', 'NOT NULL'], 
                      [COL_LOC,   'TEXT', 'NOT NULL'],
                      [COL_NAME,  'TEXT', 'NOT NULL'], 
                      [COL_LAST,  'TEXT', 'NOT NULL'],
                      [COL_COUNT, 'TEXT', 'NOT NULL'],
                      [COL_FAV,   'TEXT', 'NOT NULL']
                     ]
GEN_TABLE_KEY = [COL_PN, COL_LOC]
