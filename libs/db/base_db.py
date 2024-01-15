from .common import *
import sqlite3
import re
import os
import shutil
import threading
from log.log import log as logger

class base_db:

  def __init__(self, db_dir, db_name, log=None, lock=None, debug=False):
    ''' initialize database
      Arguments
      ---------
        db_file - database file
        log - logger
        debug - debug enabled
    '''
    self.db_name = db_name
    self.db_file_name = os.path.join(db_dir, db_name +".db")

    if log is None:
      self.log = logger(log_dir='', log_name='main_log', debug=debug)
    else:
      self.log = log

    # multithread resource lock
    if lock is None:
      self.lock = threading.Lock() 
    else:
      self.lock = lock

    self.debug = debug
    if debug:
      self.debug_db_name = db_name + "_debug"
      self.debug_db_file_name = os.path.join(db_dir, db_name + "_debug.db")
    self.create_db()

  def create_db(self):
    ''' create database
    '''

    # create database or connect to existed one
    if os.path.isfile(self.db_file_name):
      if self.debug:
        # debug mode: copy the db to debug db, and operate the debug db
        shutil.copy(self.db_file_name, self.debug_db_file_name)
        self.log.info('Connect Existing Database %s' % self.debug_db_file_name)
      else:
        self.log.info('Connect Existing Database %s' % self.db_file_name)
    else:
      if self.debug:
        self.log.info('Create New Database %s' % self.debug_db_file_name)
      else:
        self.log.info('Create New Database %s' % self.db_file_name )
    if self.debug:
      self.db_conn = sqlite3.connect(self.debug_db_file_name)
    else:
      self.db_conn = sqlite3.connect(self.db_file_name)

  def table_exists(self, table_name):
    ''' Whether table exists
      Arguments
      ---------
        table_name - table name
      Returns 
      ---------
        exist
    '''
    cmd = 'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="%s";' % table_name
    (success, results) = self.execute_sql_cmd(cmd, err_waive_list=[ 'no such table: %s' % table_name])
      
    if success and results[0][0]==1 : 
      return True
    else:
      return False

  def create_table(self, table_name, table_schema, primary_key, initial_db = False):
    ''' Create table
      Arguments
      ---------
        table_name - table name
        table_schem - table columns list, the list is two-dimension list, e.g. [[COLUMN_NAME, DATATYPE, NOT NULL(if need)], [], []]
        primary_key - primary key list, the list is one-dimension list
        initial_db - initialize database, delete previous entries if exists
      Returns 
      ---------
        (success, cursor)
    '''
    cmd_list = ['CREATE', 'TABLE', 'IF', 'NOT', 'EXISTS', table_name, '(']
    for column in table_schema:
      for arg in column:
        cmd_list.append(arg)
  
      cmd_list.append(',')
  
    cmd_list.append('PRIMARY')
    cmd_list.append('KEY')
    cmd_list.append('(')
    for arg in primary_key:
      cmd_list.append(arg)
      cmd_list.append(',')

    if cmd_list[-1] == ',':
      cmd_list.pop(-1)
  
    cmd_list.append(')')
    cmd_list.append(')')
    cmd_list.append(';')
  
    cmd = ' '.join(cmd_list)
    (success, c) = self.execute_sql_cmd(cmd)

    if initial_db and success:
      return self.clear_table(table_name)

    return success

  def delete_table(self, table_name):
    ''' detele table
      Arguments
      ---------
        table_name - table name
      Returns 
      ---------
        success
    
    '''
    cmd_list = ['DROP', 'TABLE']
    cmd_list.append(table_name)
    cmd_list.append(';')

    cmd = ' '.join(cmd_list)

    (success, c) = self.execute_sql_cmd(cmd, err_waive_list=[ 'no such table: %s' % table_name])
    return success

  def clear_table(self, table_name):
    ''' detele all entries in a table 
      Arguments
      ---------
        table_name - table name
      Returns 
      ---------
        success
    
    '''
    return self.delete_row(table_name, cond='')

  def add_row(self, table_name, table_row):
    ''' Create table entry
      Arguments
      ---------
        table_name - table name
        table_row - table entry will added in dict, e.g. {column, value}
      Returns 
      ---------
        (success, cursor)
    '''

    cmd_list = ['INSERT', 'INTO', table_name]

    schema_list = ['(']
    value_list = ['(']

    for key in table_row:
      schema_list.append(key)
      schema_list.append(',')
      value_list.append(self.format_string(table_row[key]))
      value_list.append(',')

    # pop last ","
    if schema_list[-1] == ',':
      schema_list.pop(-1)
    if value_list[-1] == ',':
      value_list.pop(-1) 

    # close bracket
    schema_list.append(')')
    value_list.append(')')

    cmd_list = cmd_list + schema_list
    cmd_list.append('VALUES')
    cmd_list = cmd_list + value_list
    cmd_list.append(';')

    cmd = ' '.join(cmd_list)
    (success, c) = self.execute_sql_cmd(cmd)
    return success

  def delete_row(self, table_name, prm = {}, exac_match = True, cond = ''):
    ''' detele entry in a table 
      Arguments
      ---------
        table_name- table name
        prm - primary key
        cond - condition, if matching condition is complict
      Returns 
      ---------
        success
    '''
    cmd_list = ['DELETE', 'FROM', table_name]
    cmd_list += self.format_condition(prm, exac_match, cond)
    cmd_list.append(';')

    cmd = ' '.join(cmd_list)

    (success, c) = self.execute_sql_cmd(cmd, err_waive_list=[ 'no such table: %s' % table_name])
    return success

  def total_row_count(self, table_name):
    ''' return total row count
      Arguments
      ---------
        table_name- table name
      Returns 
      ---------
        success
    '''
    cmd_list = ['SELECT', 'COUNT', '(*)', 'FROM']
    cmd_list.append(table_name)
    cmd_list.append(';')

    cmd = ' '.join(cmd_list)

    (success, c) = self.execute_sql_cmd(cmd, err_waive_list=[ 'no such table: %s' % table_name])
    if success:
      return c[0][0]
    else:
      return 0


  def row_exists(self, table_name, prm={}, exact_match=True, cond=''):
    ''' check whether the row exists
      Arguments
      ---------
        table_name - table name
        prm - primary key and value
        cond - condition, if matching condition is complict
      Returns 
      ---------
        exists
    '''
    cmd_list = ['SELECT ', 'EXISTS', '(', 'SELECT', '1', 'FROM', table_name]
    cmd_list += self.format_condition(prm, exact_match, cond)
    cmd_list.append(');')

    cmd = ' '.join(cmd_list)

    (success, c) = self.execute_sql_cmd(cmd, err_waive_list=[ 'no such table: %s' % table_name])
    if success and c[0][0] == 1:
      return True
    else :
      return False

  def get_col(self, table_name, col=[], prm = {}, exact_match=True, cond = ''):
    ''' Get entry value
      Arguments
      ---------
        table_name - table name
        col - column list, list of column name want to get 
        prm - primary key, dict, key column's name and value
        exact_match - exact match the prm
        cond - conddition of the select if complicated and prm can not reach goal
      Returns 
      ---------
        (success, value list)
    '''
    cmd_list = ['SELECT']

    for c in col:
      cmd_list.append(c)
      cmd_list.append(',')

    if cmd_list[-1] == ",":
      cmd_list.pop(-1) 
    
    cmd_list.append('from')
    cmd_list.append(table_name)
    cmd_list += self.format_condition(prm, exact_match, cond)
    cmd_list.append(';')

    cmd = ' '.join(cmd_list)

    (success, results ) = self.execute_sql_cmd(cmd, err_waive_list=[ 'no such table: %s' % table_name])
    if success:
      if len(results) > 0:
        return (True, results)
      else:
        return (False, [])  
    else:
      return(False, [])

  def get_col_from_sngl_row(self, table_name, col, prm = {}, exact_match=True, cond = ''):
    ''' Get column entry value, and only one row can match
      Arguments
      ---------
        table_name - table name
        col - column name
        prm - primary key, dict, key column's name and value
        exact_match - exact match the prm
        cond - conddition of the select if complicated and prm can not reach goal
      Returns 
      ---------
        (success, value string)
    '''
    success = None
    rcol = None
    if isinstance(col, str):
      (success, rcol) = self.get_col(table_name=table_name, col=[col], prm=prm, exact_match=exact_match, cond=cond)
    else: 
      (success, rcol) = self.get_col(table_name=table_name, col=col, prm=prm, exact_match=exact_match, cond=cond)

    if success: 
      if len (rcol) == 0:
        self.log.error("Can not find Column {}, from row match with condition {}".format(str(col), self.format_condition(prm, exact_match, cond)))
        return (False, [])
      elif len (rcol) > 1:
        self.log.error("Find out more than 1 row match with condition {}".format(self.format_condition(prm, exact_match, cond)))
        return (False, [])
      else:
        return (True, list(rcol[0]))
        
    else:  
      self.log.error("Cannot find out any row match with condition {}".format(self.format_condition(prm, exact_match, cond)))
      return (False, "")


  def get_sngl_col_from_sngl_row(self, table_name, col, prm = {}, exact_match=True, cond = ''):
    ''' Get column entry value, and only one row can match
      Arguments
      ---------
        table_name - table name
        col - column name
        prm - primary key, dict, key column's name and value
        exact_match - exact match the prm
        cond - conddition of the select if complicated and prm can not reach goal
      Returns 
      ---------
        (success, value string)
    '''
    (success, rcol) = self.get_col_from_sngl_row(table_name=table_name, col=[col], prm=prm, exact_match=exact_match, cond=cond)
    if success:
      return rcol[0]
    else: 
      return ""

  def update_col(self, table_name, col = {}, prm = {}, exact_match=True, cond = ''):
    ''' Get entry value
      Arguments
      ---------
        table_name - table name
        col - dict, column's name and to be added value of the column
        prm - primary key, dict, key column's name and value
        exact_match - exact match the prm
        cond - conddition of the select if complicated and prm can not reach goal
      Returns 
      ---------
        success
    '''
    cmd_list = ["UPDATE", table_name, "SET"]

    for c in col :
      cmd_list.append(c)
      cmd_list.append("=")
      cmd_list.append(self.format_string(col[c]))
      cmd_list.append(",")

    if cmd_list[-1] == ",":
      cmd_list.pop(-1)
    
    cmd_list += self.format_condition(prm, exact_match, cond)
    cmd_list.append(';')

    cmd = ' '.join(cmd_list)

    (success, results ) = self.execute_sql_cmd(cmd, err_waive_list=[ 'no such table: %s' % table_name])
    return success

  def add_to_col_from_sngl_row(self, table_name, col = {}, prm = {}, exact_match=True, cond = ''):
    ''' Add new value to existing column entry, which is list, only support single row here
      Arguments
      ---------
        table_name - table name
        col - dict, column's name and to be added value of the column
        prm - primary key, dict, key column's name and value
        exact_match - exact match the prm
        cond - conddition of the select if complicated and prm can not reach goal
      Returns 
      ---------
        success
    '''

    cl = list(col.keys())
    (success, rcol) = self.get_col_from_sngl_row(table_name, cl, prm, exact_match, cond)   

    if success:
      for i in range(len(cl)):
        c = cl[i]
        vl = self.string2list(rcol[i])
        while("" in vl):
          vl.remove("")
        if isinstance (col[c], list):
          for v in col[c]:
            if v not in vl and v != "":
              vl.append(v)
        elif isinstance (col[c], str):
          if col[c] not in vl and col[c] != "":
            vl.append(col[c])
        else:
          self.log.error("Not support add {} type to exist column".format(type(col[c])))
          return False
        col[c] = vl

      return self.update_col(table_name, col, prm, exact_match, cond)
    else:
      return False

  def inc_sngl_col_from_sngl_row(self, table_name, col, v=1, prm = {}, exact_match=True, cond = ''):
    ''' Increase the value of single column from single row
      Arguments
      ---------
        table_name - table name
        col - column's name 
        v - to be increased value of the column
        prm - primary key, dict, key column's name and value
        exact_match - exact match the prm
        cond - conddition of the select if complicated and prm can not reach goal
      Returns 
      ---------
        success
    '''

    rcol = self.get_sngl_col_from_sngl_row(table_name, col, prm, exact_match, cond)   
    try: 
      rcol_i = int(rcol)
      rcol_i += v
      return self.update_col(table_name, {col: rcol_i}, prm, exact_match, cond)
    except ValueError:
      self.log.error("Can not convert {} to int".format(col))
      return False


     


  def del_from_col(self, table_name, col = {}, prm = {}, exact_match=True, cond = ''):
    ''' delete value from existing column entry, which is list
      Arguments
      ---------
        table_name - table name
        col - dict, column's name and to be added value of the column
        prm - primary key, dict, key column's name and value
        exact_match - exact match the prm
        cond - conddition of the select if complicated and prm can not reach goal
      Returns 
      ---------
        success
    '''

    cl = list(col.keys())
    (success, rcol) = self.get_col_from_sngl_row(table_name, cl, prm, exact_match, cond)   

    if success:
      for i in range(len(cl)):
        c = cl[i]
        vl = self.string2list(rcol[i])
        while("" in vl):
          vl.remove("")
        if isinstance (col[c], list):
          for v in col[c]:
            try:
              vl.remove(v)
            except ValueError:
              pass  # do nothing!
        elif isinstance (col[c], str):
          try:
            vl.remove(col[c])
          except ValueError:
            pass  # do nothing!
        else:
          self.log.error("Not support remove {} type to exist column".format(type(col[c])))
          return False
        col[c] = vl

      return self.update_col(table_name, col, prm, exact_match, cond)
    else:
      return False
       
  def list2string(self, l):
    ''' convert list to string
      Arguments
      ---------
        l - list
      Returns
      ---------
        s - string
    '''
    return LIST_SEP.join(l)

  def string2list(self, s):
    ''' convert string to list
      Arguments
      ---------
        s - string
      Returns
      ---------
        l - list
    '''
    return s.split(LIST_SEP)


  def format_string(self, ori):
    ''' format string to sql
      Arguments
      ---------
        ori - original 
      Returns
      ---------
        fstr - formated string
    '''
    if isinstance(ori, list):
      ori = self.list2string(ori)
    return "\"" + str(ori) + "\""

  def format_condition(self, m_dict={}, exact_match=True, comp_cond=''):
    ''' format condition in list
      Arguments
      ---------
        m_dict - matching dict
        exac_match - exact match or not
        comp_cond - complicated condition
      Returns 
      ---------
        cond_list
    '''
    cond_list = []
    if len(comp_cond) > 0:
      cond_list.append("where")
      cond_list.append(comp_cond)
    elif len(m_dict) > 0:
      cond_list.append("where")
      for key in m_dict:
        cond_list.append(key)
        if exact_match:
          cond_list.append("=")
        else:
          cond_list.append("like")
        cond_list.append(self.format_string(m_dict[key]))
        cond_list.append("and")

      if cond_list[-1] == "and":
        cond_list.pop(-1)
    
    return cond_list

 
  def execute_sql_cmd(self, cmd, err_waive_list=[]):
    ''' Execute sql command
      Arguments
      ---------
        cmd - sql command
        err_waive_list - the list of waiver format when error encountered executing sql command

      Returns 
      ---------
        (success, cursor)
    '''
  
    # lock not accessable by others
    if self.lock:
      self.lock.acquire()
    self.log.debug( "%s executing Sql command: %s" % (self.db_name, cmd))

    c = self.db_conn.cursor()
    try:
      # execute the sql command
      cursor = c.execute(cmd)
      self.db_conn.commit()

      results = cursor.fetchall()
      return (True, results)
    except sqlite3.Error as e:
      err_msg = ' '.join(e.args)
      # filt error message with waivers
      for waiver in err_waive_list:
        if re.match(waiver, err_msg):
          return (False, None)
  
      self.log.error('SQLite command \'%s\' error: %s' % (cmd, err_msg))
      return (False, None)
    finally:
      # release lock 
      if self.lock:
        self.lock.release()
      else:
        pass
