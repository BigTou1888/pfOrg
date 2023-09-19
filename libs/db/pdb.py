import os

COL_PN = 'pn'
COL_LOC = 'location'
COL_NAME = 'name'
COL_FL = 'filelist'
COL_ACT = 'actress'
COL_GEN = 'genre'
COL_TIME = 'time'
COL_COMPANY = 'company'

MAIN_TABLE = 'main'
MAIN_TABLE_SCHEMA = [[COL_PN, 'TEXT', 'NOT NULL'], 
                     [COL_LOC, 'TEXT', 'NOT NULL'], 
                     [COL_NAME, 'TEXT', 'NOT NULL'], 
                     [COL_FL, 'TEXT', 'NOT NULL'], 
                     [COL_ACT, 'TEXT', 'NOT NULL'], 
                     [COL_GEN, 'TEXT', 'NOT NULL'], 
                     [COL_TIME, 'TEXT', 'NOT NULL'], 
                     [COL_COMPANY, 'TEXT', 'NOT NULL']]
MAIN_TABLE_KEY = [COL_PN, COL_LOC]
UNKNOWN_TABLE = 'unknown'
UNKNOWN_TABLE_SCHEMA = [[COL_LOC, 'TEXT', 'NOT NULL'], 
                     [COL_NAME, 'TEXT', 'NOT NULL'], 
                     [COL_FL, 'TEXT', 'NOT NULL'], 
                     [COL_ACT, 'TEXT', 'NOT NULL'], 
                     [COL_GEN, 'TEXT', 'NOT NULL'], 
                     [COL_TIME, 'TEXT', 'NOT NULL'], 
                     [COL_COMPANY, 'TEXT', 'NOT NULL']]
UNKNOWN_TABLE_KEY = [COL_LOC]
ACT_TABLE = 'actress'
ACT_TABLE_SCHEMA = [ [COL_ACT, 'TEXT', 'NOT NULL'], 
                     [COL_PN, 'TEXT', 'NOT NULL'], 
                     [COL_LOC, 'TEXT', 'NOT NULL']]
ACT_TABLE_KEY = [COL_ACT]
GEN_TABLE = 'genre'
GEN_TABLE_SCHEMA = [ [COL_GEN, 'TEXT', 'NOT NULL'], 
                     [COL_PN, 'TEXT', 'NOT NULL'], 
                     [COL_LOC, 'TEXT', 'NOT NULL']]
ACT_TABLE_KEY = [COL_GEN]
class pfd(Database):
    def __init__(self, name='', log=None, dbDir='sql', dbName='pdb', initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=False, cacheEntries=0):
        if dbDir == '':
            self.dbDir = os.getcwd()
        else:
            self.dbDir = dbDir
        super().__init__(name=dbName, log=log, dbDir=self.dbDir, dbName=dbName, initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=selfLock, cacheEntries=cacheEntries)

        if not self.tableExists(MAIN_TABLE):
            self.createTable(MAIN_TABLE, MAIN_TABLE_SCHEMA, MAIN_TABLE_KEY)
        if not self.tableExists(UNKNOWN_TABLE):
            self.createTable(UNKNOWN_TABLE, UNKNOWN_TABLE_SCHEMA, UNKNOWN_TABLE_KEY)
        if not self.tableExists(ACT_TABLE):
            self.createTable(ACT_TABLE, ACT_TABLE_SCHEMA, ACT_TABLE_KEY)
        if not self.tableExists(GEN_TABLE):
            self.createTable(GEN_TABLE, GEN_TABLE_SCHEMA, GEN_TABLE_KEY)

    def add_new_pn(self, pn, loc='', name='', filelist=[], actress=[], gen=[], time='', company=''):
