
import os
import sqlite3
from datetime import datetime
import threading
import re


class base_db():

  def __init__(self, name='', log=None, dbDir='dbs', dbName='csr', initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=False, cacheEntries=0):
    ''' Initialize a new database wrapper.

    Arguments
    ---------

    name
      name of component

    log
      logger class

    dbDir
      database directory

    dbName
      database name

    initNewDb
      initialize the database

    appendTime
      append time suffix after teh dbName

    maxHistDbs
      the maximum number of history database

    '''
    super().__init__(name, log)
    self.dbDir = dbDir
    self.dbName = dbName
    self.initNewDb = initNewDb
    self.appendTime = appendTime
    self.maxHistDbs = maxHistDbs
    self.selfLock= selfLock
    if self.selfLock:
      self.lock = threading.Lock()

    if appendTime:
      self.dbFileName = os.path.join(dbDir, dbName + '_' + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.db')
    else:
      self.dbFileName = os.path.join(dbDir, dbName + '.db')

    self.mDb = self.getDb()

    self.cmdCache = cacheDict(cacheEntries)
    
  def createDb(self, initNewDb=False):
    ''' create database
  
    Returns 
    ---------

    db
      database created
    '''

    # clean the db directory, create the directory if not exists, if the history dbs exceed the maximum, delete the old ones
    self.dirClean(initNewDb)
    # create database or connect to existed one
    if os.path.isfile(self.dbFileName):
      self.log.info(0, 'Connect Existing Database %s' % self.dbFileName)
    else:
      self.log.info(0, 'Create New Database %s' % self.dbFileName)
    db_conn = sqlite3.connect(self.dbFileName, check_same_thread=False)
    return db_conn

  def getDb(self):
    ''' get database created, if not exist, create a new one
  
    Returns 
    ---------

    db
      database
    '''
    if not hasattr(self, 'mDb'):
      self.mDb = self.createDb(self.initNewDb)
    return self.mDb

  def dirClean(self, initNewDb=False):
    ''' Clean log directory, if the old logs exceed the maximum logs, delete the oldest '''
    # if the directory does not exist, create a new one
    if not os.path.exists(self.dbDir):
      #os.mkdir(self.dbDir)
      os.makedirs(self.dbDir, exist_ok=True)

    if initNewDb:
      # only checking history dbs when initNewDb is not set
      # if the history logs exceed maximum limit, delete old ones
      oldDbs = [os.path.join(self.dbDir, f) for f in os.listdir(self.dbDir) if
                os.path.isfile(os.path.join(self.dbDir, f)) and f.startswith(self.dbName)]
      oldDbs.sort()
      while len(oldDbs) >= self.maxHistDbs and len(oldDbs) != 0:
        # remove oldest dbs, if exceed the limit
        os.remove(oldDbs[0])
        oldDbs.pop(0)

  def executeSqlCmd(self, cmd, errWaiverList=[]):
    ''' Execute sql command

    Arguments
    ---------

    cmd
      command

    errWaiverList
      the list of waiver format when error encountered executing sql command

    Returns 
    ---------
      (success, cursor)

    
    '''
  
    # lock not accessable by others
    if self.selfLock:
      self.lock.acquire()
    #self.log.debug( "%s executing Sql command: %s" % (self.dbName, cmd))

    (cacheHit, cacheResult) = self.cmdCache.getResult(cmd)

    if cacheHit:
      self.log.debug("%s cache hits" % cmd)
      return cacheResult
    else:
      self.log.debug("%s cache not hits" % cmd)
      c = self.mDb.cursor()
      try:
        # execute the sql command
        cursor = c.execute(cmd)
        self.mDb.commit()

        results = cursor.fetchall()
        self.cmdCache.updDict(cmd, (True, results))
        return (True, results)
      except sqlite3.Error as e:
        errMsg = ' '.join(e.args)
        # filt error message with waivers
        for waiver in errWaiverList:
          if re.match(waiver, errMsg):
            self.cmdCache.updDict(cmd, (False, None))
            return (False, None)
  
        self.log.error('SQLite command \'%s\' error: %s' % (cmd, errMsg))
        self.cmdCache.updDict(cmd, (False, None))
        return (False, None)
      finally:
        # release lock 
        if self.selfLock:
          self.lock.release()
        else:
          pass
  
  def createTable(self, tableName, tableSchema, primaryKey, initialDb = False):
    ''' Create table

    Arguments
    ---------

    tableName
      table name

    tableSchema
      table columns list, the list is two-dimension list, e.g. [[COLUMN_NAME, DATATYPE, NOT NULL(if need)], [], []]

    primaryKey
      primary key list, the list is one-dimension list

    Returns 
    ---------

      (success, cursor)
    
    '''

    cmdList = ['CREATE', 'TABLE', 'IF', 'NOT', 'EXISTS', tableName, '(']
    for column in tableSchema:
      for arg in column:
        cmdList.append(arg)
  
      cmdList.append(',')
  
    cmdList.append('PRIMARY')
    cmdList.append('KEY')
    cmdList.append('(')
    for arg in primaryKey:
      cmdList.append(arg)
      cmdList.append(',')
  
    if cmdList[-1] == ',':
      cmdList.pop(-1)
  
    cmdList.append(')')
    cmdList.append(')')
    cmdList.append(';')
  
    cmd = ' '.join(cmdList)
    (success, c) = self.executeSqlCmd(cmd)

    if initialDb and success:
      return self.deleteAllEntries(tableName)

    return success

  def createEntry(self, tableName, tableRow):
    ''' Create table entry

    Arguments
    ---------

    tableName
      table name

    table row
      table entry will added in dict, e.g. {column, value}

    Returns 
    ---------

      (success, cursor)
    
    '''

    cmdList = ['INSERT', 'INTO', tableName, '(']

    schemaList = []
    valueList = []

    for key in tableRow:
      schemaList.append(key)
      schemaList.append(',')
      valueList.append(tableRow[key])
      valueList.append(',')

    schemaList.pop(-1)
    valueList.pop(-1)

    cmdList = cmdList + schemaList
    cmdList.append(')')
    cmdList.append('VALUES')
    cmdList.append('(')
    cmdList = cmdList + valueList
    cmdList.append(')')
    cmdList.append(';')

    cmd = ' '.join(cmdList)
    (success, c) = self.executeSqlCmd(cmd)
    return success

  def deleteEntry(self, tableName, cond):
    ''' detele entry in a table 

    Arguments
    ---------

    tableName
      table name

    cond
      condition

    Returns 
    ---------

      success
    
    '''

    cmdList = ['DELETE', 'FROM', tableName]
    if cond != '':
      cmdList.append('where')
      cmdList.append(cond)
    cmdList.append(';')

    cmd = ' '.join(cmdList)

    (success, c) = self.executeSqlCmd(cmd, errWaiverList=[ 'no such table: %s' % tableName])
    return success

  def deleteAllEntries(self, tableName):
    ''' detele all entries in a table 

    Arguments
    ---------

    tableName
      table name

    Returns 
    ---------

      success
    
    '''

    '''
    cmdList = ['DELETE', 'FROM', tableName]
    cmd = ' '.join(cmdList)
    (success, c) = self.executeSqlCmd(cmd)
    return success
    '''
    return self.deleteEntry(tableName, cond='')


  def tableExists(self, tableName):
    ''' Whether table exists

    Arguments
    ---------

    tableName
      table name

    Returns 
    ---------

      exist
    
    '''
    cmd = 'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="%s";' % tableName
    (success, results) = self.executeSqlCmd(cmd, errWaiverList=[ 'no such table: %s' % tableName])

      
    if success and results[0][0]==1 : 
      return True
    else:
      return False

  def getEntryValue(self, tableName, entryList, cond = ''):
    ''' Get entry value

    Arguments
    ---------

    tableName
      table name

    entryList
      list of column name want to get 

    cond
      conddition of the select  command

    Returns 
    ---------

      (success, value list)
    
    '''
    cmdList = ['SELECT']

    for entry in entryList :
      cmdList.append(entry)
      cmdList.append(',')

    cmdList.pop(-1)
    
    cmdList.append('from')
    cmdList.append(tableName)
    if cond != '':
      cmdList.append('where')
      cmdList.append(cond)
    cmdList.append(';')
    cmd = ' '.join(cmdList)
    (success, results ) = self.executeSqlCmd(cmd, errWaiverList=[ 'no such table: %s' % tableName])
    if success:
      if len(results) > 0:
        return (True, results)
      else:
        return (False, [])  
    else:
      return(success, [])

  def getFirstEntryValue(self, tableName, entryList, cond = ''):
    ''' Get first entry value
    Arguments
    ---------

    tableName
      table name

    entryList
      list of column name want to get 

    cond
      conddition of the select  command

    Returns 
    ---------

      (success, value list)
    

    '''
    (success, results) = self.getEntryValue(tableName, entryList, cond)

    if success:
      return (True, results[0])
    else:
      return(False, None)

  def updateEntryValue(self, tableName, entryValues, cond = ''):
    ''' Update entry value

    Arguments
    ---------

    tableName
      table name

    entryValues
      dictionary of column name and value

    cond
      conddition of the select  command

    Returns 
    ---------

      success
    
    '''
    cmdList = ['UPDATE', tableName, 'SET']

    for entry in entryValues:
      value = entryValues[entry]
      cmdList.append(entry)
      cmdList.append('=')
      cmdList.append(value)
      cmdList.append(',')

    # pop last ','
    cmdList.pop(-1)
    
    if cond != '':
      cmdList.append('WHERE')
      cmdList.append(cond)
    cmdList.append(';')
    cmd = ' '.join(cmdList)
    (success, c) = self.executeSqlCmd(cmd)
    return success

  def updateOrCreateEntryValue(self, tableName, entryValues):
    ''' Update entry value, if not exists, create the entry

    Arguments
    ---------

    tableName
      table name

    entryValues
      dictionary of column name and value

    Returns 
    ---------

      success
    
    '''
    cmdList = ['INSERT', 'OR', 'REPLACE', 'INTO', tableName]
    cmdList.append('(')


    for entry in entryValues:
      cmdList.append(entry)
      cmdList.append(',')

    # pop last ','
    cmdList.pop(-1)
    cmdList.append(')')

    cmdList.append('VALUES')
    cmdList.append('(')


    for entry in entryValues:
      #value = entryValues[entry]
      #cmdList.append(str(value))
      value = self.sqlStringTypeConvert(entryValues[entry])
      cmdList.append(value)
      cmdList.append(',')

    # pop last ','
    cmdList.pop(-1)
    cmdList.append(')')
    
    cmdList.append(';')
    cmd = ' '.join([str(x) for x in cmdList])
    (success, c) = self.executeSqlCmd(cmd)
    return success

  def sqlStringTypeConvert(self, value):
    # quote value with "/', if the value is string
    # if the value type is not string, does not change

    if type(value) == type('string'):
      if value.startswith('\'') and value.endswith('\'') :
        # if quote with '' already, does not change
        return value
      elif value.startswith('"') and value.endswith('"') :
        # if quote with "" already, does not change
        return value
      else: 
        if ('\'' in value) and ('"' in value):
          # if the value contains both ' and ", report error
          self.log.error('%s mix \' and "' % value)
          return value
        elif '"' in value:
          # if the value contains ", quote with '
          return '\'' + value + '\''
        else:
          # if the value does not contains ", quote with "
          return '"' + value + '"'

    else:
      return value
      
