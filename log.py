import os
from datetime import datetime
import logging


class Log ():
  '''
    The logger wrapper

    Attributes
    ----------
    logName
      log name, log component name and log file prefix name

    logDir = logDir
      log file directory

    maxHistLogs = maxHistLogs
      the maximum number of history log files

    logLevel
      logging level

    logFileName
      log file name

    logFormat 
      log format, prefix prepend

    logFileMode
      log file mode, fix to 'w'

    logger
      logger

    Methods
    -------

    __init__
      Initialize a new logger

    createLogger
      create logger

    getLogger
      get logger, if not exist, create a new one

    dirClean
      Clean log dictory, if the old logs exceed the maximum logs, delete the oldest

    info
      log message as info 

    debug
      log message as debug, verbosity set 6 for klog

    error
      log message as error

  '''

  def __init__(self, logName='default', logDir='logs', appendTime=False, maxHistLogs=1, debug=True):
    ''' Initialize a new crashdump core.
  
    Arguments
    ---------
  
    logName
      name of the logger and log file name
  
    logDir
      log file directory

    maxHistLogs
      the maximum number of history log files
      
    debug
      debug mode, it will affect log level
    '''

    self.logName = logName
    self.logDir = logDir
    self.appendTime = appendTime
    self.maxHistLogs = maxHistLogs

    if maxHistLogs > 1:
      self.appendTime = True

    if debug:
      self.logLevel = logging.DEBUG
    else:
      self.logLevel = logging.INFO

    if self.appendTime:
      self.logFileName = os.path.join(self.logDir, self.logName + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log')
    else:
      self.logFileName = os.path.join(self.logDir, self.logName + '.log')

    self.logFormat ='%(asctime)s : %(levelname)s : %(message)s'
    self.logFileMode = 'w'

    self.logger = self.getLogger()

  def createLogger(self):
    ''' create logger
  
    Returns 
    ---------

    logger
      logger created
    '''

    # clean the log directory, create the directory if not exists, if the history logs exceed the maximum, delete the old ones
    self.dirClean()
    # create logger
    logger = logging.getLogger(self.logName)
    logging.basicConfig(level=self.logLevel, filename=self.logFileName, format=self.logFormat, filemode=self.logFileMode)

    return logger

  def getLogger(self):
    ''' get logger, if not exist, create a new one
  
    Returns 
    ---------

    logger
      logger created
    '''
    if not hasattr(self, 'logger'):
      self.logger = self.createLogger()
    return self.logger

  def dirClean(self):
    ''' Clean log dictory, if the old logs exceed the maximum logs, delete the oldest '''
    # if the directory does not exist, create a new one
    if not os.path.exists(self.logDir):
      #os.mkdir(self.logDir)
      os.makedirs(self.logDir, exist_ok=True)

    # if the history logs exceed maximum limit, delete old ones
    oldLogs = [os.path.join(self.logDir, f) for f in os.listdir(self.logDir) if os.path.isfile(os.path.join(self.logDir, f)) and f.startswith(self.logName)]
    oldLogs.sort()
    while len(oldLogs) >= self.maxHistLogs and len(oldLogs) != 0:
      # remove oldest logs, if exceed the limit
      os.remove(oldLogs[0])
      oldLogs.pop(0)

  def info(self, msg):
    ''' log message as info 

    Arguments
    ---------
  
    msg
      log message
 
    '''

    self.logger.info(msg)

  def debug(self, msg):
    ''' log message as debug
        verbosity set 6 for klog

    Arguments
    ---------
  
    msg
      log message
 
    '''
    self.logger.debug(msg)

  def error(self, msg):
    ''' log message as error

    Arguments
    ---------
  
    msg
      log message
 
    '''
    self.logger.error(msg)

  def warning(self, msg):
    ''' log message as debug
        verbosity set 6 for klog

    Arguments
    ---------
  
    msg
      log message
 
    '''

    self.logger.warning(msg)
