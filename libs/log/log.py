import os
from datetime import datetime
import logging


class log ():

  def __init__(self, log_dir='logs', log_name='default', append_time=False, max_hist_logs=1, debug=True):
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

    self.log_name = log_name
    self.log_dir = log_dir
    self.append_time = append_time
    self.max_hist_logs = max_hist_logs

    if max_hist_logs > 1:
      self.append_time = True

    if debug:
      self.log_lvl = logging.DEBUG
    else:
      self.log_lvl = logging.INFO

    if self.append_time:
      self.log_file_name = os.path.join(self.log_dir, self.log_name + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log')
    else:
      self.log_file_name = os.path.join(self.log_dir, self.log_name + '.log')

    self.log_format ='%(asctime)s : %(levelname)s : %(message)s'
    self.log_file_mode = 'w'

    self.logger = self.get_logger()

  def create_logger(self):
    ''' create logger
  
    Returns 
    ---------

    logger
      logger created
    '''

    # clean the log directory, create the directory if not exists, if the history logs exceed the maximum, delete the old ones
    self.dir_clean()
    # create logger
    logger = logging.getLogger(self.log_name)
    logging.basicConfig(level=self.log_lvl, filename=self.log_file_name, format=self.log_format, filemode=self.log_file_mode)

    return logger

  def get_logger(self):
    ''' get logger, if not exist, create a new one
  
    Returns 
    ---------

    logger
      logger created
    '''
    if not hasattr(self, 'logger'):
      self.logger = self.create_logger()
    return self.logger

  def dir_clean(self):
    ''' Clean log dictory, if the old logs exceed the maximum logs, delete the oldest '''
    # if the directory does not exist, create a new one
    if not os.path.exists(self.log_dir):
      #os.mkdir(self.logDir)
      os.makedirs(self.log_dir, exist_ok=True)

    # if the history logs exceed maximum limit, delete old ones
    oldLogs = [os.path.join(self.log_dir, f) for f in os.listdir(self.log_dir) if os.path.isfile(os.path.join(self.log_dir, f)) and f.startswith(self.log_name)]
    oldLogs.sort()
    while len(oldLogs) >= self.max_hist_logs and len(oldLogs) != 0:
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
