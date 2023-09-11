# -*- mode: python -*-

# Zyzyx, Inc. CONFIDENTIAL 
# Copyright 2021 Zyzyx, Inc. All Rights Reserved.
#
# NOTICE: All information contained herein is the property of Zyzyx, Inc. and
# its suppliers if any.  The intellectual and technical concepts contained
# herein are proprietary to Zyzyx, Inc. and its suppliers and may be covered
# by U.S. and foreign patents or patents in process, and are protected by
# trade secret or copyright law.  Dissemination of this information or
# reproduction of this material is strictly forbidden without prior written
# permission from Zyzyx, Inc.

''' Module for logging, can switch between python built-in logging and klog used in fiji_pdk or both.

Classes
-------

Log
    The logger wrapper

'''

import os
from datetime import datetime
import logging

klogImported = True
try:
  import klog
except ImportError:
  klogImported = False





class Log ():
  '''
    The logger wrapper

    Attributes
    ----------
    logName
      log name, log component name and log file prefix name

    logType
      log type, can be 'logging', 'klog', and 'both'

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

  def __init__(self, logName='default', logType='logging', logDir='logs', appendTime=False, maxHistLogs=1, debug=True, standalone=True):
    ''' Initialize a new crashdump core.
  
    Arguments
    ---------
  
    logName
      name of the logger and log file name
  
    logType
      log type, can be 'logging', 'klog', or 'both'
  
    logDir
      log file directory

    maxHistLogs
      the maximum number of history log files
      
    debug
      debug mode, it will affect log level
    '''

    self.logName = logName
    if not klogImported:
      self.logType = 'logging'
    else:
      self.logType = logType
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
    self.standalone = standalone 

    if self.logType == 'both':
      self.logger = self.getLogger()
    elif self.logType == 'logging' :
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

    if self.standalone and self.logType == 'logging':
      logger.addHandler(logging.StreamHandler())
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

  def info(self, verbosity, msg):
    ''' log message as info 

    Arguments
    ---------
  
    verbosity
      log verbosity, only effective when using klog(type is klog of both)

    msg
      log message
 
    '''

    if self.logType == 'klog':
        klog.log(verbosity, str(msg))
    elif self.logType == 'both':
        klog.log(verbosity, str(msg))
        self.logger.info(msg)
    else:
        self.logger.info(msg)

  def debug(self, msg):
    ''' log message as debug
        verbosity set 6 for klog

    Arguments
    ---------
  
    msg
      log message
 
    '''

    if self.logType == 'klog':
      klog.log(6, str(msg))
    elif self.logType == 'both':
      klog.log(6, str(msg))
      self.logger.debug(msg)
    else:
      self.logger.debug(msg)

  def error(self, msg):
    ''' log message as error

    Arguments
    ---------
  
    msg
      log message
 
    '''
    if self.logType == 'klog':
      klog.error(str(msg))
    elif self.logType == 'both':
      klog.error(str(msg))
      self.logger.error(msg)
    else:
      self.logger.error(msg)

  def warning(self, msg):
    ''' log message as debug
        verbosity set 6 for klog

    Arguments
    ---------
  
    msg
      log message
 
    '''

    if self.logType == 'klog':
      klog.log(0, 'WARN: ' + str(msg))
    elif self.logType == 'both':
      klog.log(0, 'WARN: ' + str(msg))
      self.logger.warning(msg)
    else:
      self.logger.warning(msg)


class LoggerWriter:
  # a wrapper used to replace stdio and stderr
  # when running background in bpython
  def __init__(self, logfct):
    self.logfct = logfct
    self.buf = []

  def write(self, msg):
    if msg.endswith('\n'):
      msg = msg[:-len('\n')]
      self.buf.append(msg)
      self.logfct(''.join(self.buf))
      self.buf = []
    else:
      self.buf.append(msg)

  def flush(self):
    pass

  #def isatty(self):
    #return True

