from .db import Database
from .log import Log 
from . import common
import os
import urllib.request
import re

class refInfo():
  def __init__(self):
    self.info = {}

  def addInfo(self, newInfo, parentInfo=None):
    if parentInfo is None:
      parentInfo = self.info
    for key in newInfo:
      if key in parentInfo:
        self.addInfo(newInfo[key]['next'], parentInfo[key]['next'])
      else:
        parentInfo[key] = newInfo[key]

  def getInfo(self):
    return self.info
  
class refDb(Database):
  '''

    htmlMatchTab
      Check whether the html line contains tag

    htmlExtractTabValue
      Match the html tag and extrace the value between start and end for one line

    refNameParse
      reference name parse, to get parent name and name

    refNameFormat
      reference name format from parent name and entry name

    initialRefDb
      Initialize reference Database based on HTML

    initialLbRefDb
      Initialize reference Database for LB

    refDbEntryExists
      reference database entry exists not including array index([\d])

    hierExists
      hierarchy exists

    getRefType
      Get entry type

    csrEntryExists(self, lb, csrEntryName):
      csr entry exists, full csr hierarchy name, including array index([\d])

    formatCsrName
      format csr name based on reference info

    findCsrInfo
      Find all register/field/memory/group info, based on a full hierarchy, without index([\d])

    findMemInfo
      Find memory info, includes size, virtual registers

    recursionFindGroupRegisters 
      Find registers under group in recursion way, as there may be groups under a group



  '''
  def __init__(self, log=None, dbDir='', dbName='csrRefDb', versionCheck=False, selfLock=False, cacheEntries=1000):

    if dbDir == '':
      self.dbDir = os.getcwd()
    else:
      self.dbDir = dbDir
    super().__init__(name=dbName, log=log, dbDir=self.dbDir, dbName=dbName, initNewDb=False, appendTime=False, maxHistDbs=1, selfLock=selfLock, cacheEntries=cacheEntries)
    self.versionCheck = versionCheck

  def htmlMatchTab(self, tag, line):
    ''' Check whether the html line contains tag

    Arguments
    ---------

    tag
      the html tag want to match

    line
      line data of html file

    Returns
    -------

    Found
      Found tab
    '''
    matchObj = re.match(r'.*<%s>.*' % tag, line)
    if matchObj:
      return True
    else:
      return False
  

  def htmlExtractTabValue(self, tag, line):
    ''' Match the html tag and extrace the value between start and end for one line

    Arguments
    ---------

    tag
      the html tag want to match

    line
      line data of html file

    Returns
    -------

    (Found, extractValue)
      Found tab, value extracted
    '''
    matchObj = re.match(r'.*<%s>(.*)</%s>.*' % (tag, tag), line)
    if matchObj:
      return (True, matchObj.group(1) )
    else:
      return (False, 0)

  def refNameParse(self, refName):
    ''' reference name parse
    
    Arguments
    ---------

    refName
      reference name

    Returns
    -------

    (parentName, entryName)
      
    '''
    refList = refName.split('.')
    entryName = refList.pop(-1)
    parentName = '.'.join(refList)

    return (parentName, entryName)

  def refNameFormat(self, parentName, entryName):
    ''' reference name format from parent name and entry name
    
    Arguments
    ---------

    parentName
      parent name

    entryName
      entry name

    Returns
    -------

    reference name
      
    '''
    refName = ''
    if parentName == '':
      refName = entryName
    else:
      refName = parentName + '.' + entryName

    return refName
    
  def initialRefDb(self):
    ''' Initialize reference Database based on HTML '''

    for lb in common.LB_INFO:
  
      refVersion = ''
  
      webUrl = urllib.request.urlopen(common.CSR_DEFINITION_URL + '%s_csr.html' % lb)

      # Find version from website
      for line in webUrl:
        # iterate each line of html
        line = line.decode("utf-8")
  
        (match, value) = self.htmlExtractTabValue('h2', line)
        if match:
          matchObj = re.match(r'Addressmap Information for \'%s_csr\'.*(ss-tb-.*)' % lb, value)
          if matchObj:
            refVersion = matchObj.group(1)
            break
  
      # Find version and last time update status from reference database
      # if out-of-date or last time not success, will re-initialize the database
      versionTableExist = self.tableExists('%s_version' % lb)
      statusTableExist = self.tableExists('%s_status' % lb)

      self.log.debug('Initializing lb %s' % lb)
      if versionTableExist and statusTableExist:
        self.log.debug('version table and status table exists')

        (versionSearch, versions) = self.getEntryValue('%s_version' % lb, ['"VERSION"'], '')
        (statusSearch, statuses) = self.getEntryValue('%s_status' % lb, ['"STATUS"'], '')
  
        if versionSearch and statusSearch and len(versions) > 0 and len(statuses) > 0:
            version = versions[0][0]
            status = statuses[0][0]
            self.log.debug('version is %s, status is %s' % (version, status))
  
            if ((not self.versionCheck) or (version == refVersion)) and status == 'SUCCESS':
              continue
      self.initialLbRefDb(lb)
  
  def initialLbRefDb(self, lb):
    ''' Initialize reference Database for LB

    Arguments
    ---------

    lb
      LB name
    '''

    # Create tables
    versionTableExist = self.tableExists( lb + common.CSR_REF_VERSION_TABLE_SUFFIX )

    self.createTable(tableName=( lb + common.CSR_REF_GROUP_TABLE_SUFFIX ), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_REGISTER_TABLE_SUFFIX ), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_WIDE_REGISTER_TABLE_SUFFIX ), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_SUB_WIDE_REGISTER_TABLE_SUFFIX ), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_MEMORY_TABLE_SUFFIX ), tableSchema= common.CSR_REF_MEMORY_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_WIDE_MEMORY_TABLE_SUFFIX ), tableSchema= common.CSR_REF_MEMORY_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_VIRTUAL_REGISTER_TABLE_SUFFIX ), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_VIRTUAL_WIDE_REGISTER_TABLE_SUFFIX ), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_SUB_VIRTUAL_WIDE_REGISTER_TABLE_SUFFIX ), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_FIELD_TABLE_SUFFIX), tableSchema= common.CSR_REF_REGISTER_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_CAPTURE_TABLE_SUFFIX ), tableSchema= common.CSR_REF_CAPTURE_TABLE_SCHEMA, primaryKey= common.CSR_REF_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_VERSION_TABLE_SUFFIX ), tableSchema= common.CSR_REF_VERSION_TABLE_SCHEMA, primaryKey= common.CSR_REF_VERSION_TABLE_PRIMARY_KEY)
    self.createTable(tableName=( lb + common.CSR_REF_STATUS_TABLE_SUFFIX ), tableSchema= common.CSR_REF_STATUS_TABLE_SCHEMA, primaryKey= common.CSR_REF_STATUS_TABLE_PRIMARY_KEY)

    hierList = []
  
    csrRefList = parseHtmlInfo(lb)
    self.log.debug(str(csrRefList))
    for entry in csrRefList:
      entryName = entry[0]
      entryRefName = entry[1]
      typeName = entry[2]
      entryAccess = entry[3]
      entryArrayed = entry[4]
      entrySize = entry[5]
      entryCapture = entry[6]
      tableName = lb + '_' + entry[2]

      entryRefList = entryRefName.split('.')

      if entryRefList[0] == (lb + '_csr') :
        entryRefList.pop(0)

      if entryRefList[-1] == entryName:
        entryRefList.pop(-1)

      entryParentName = '.'.join(entryRefList)
  
  
      if typeName == 'memory' or typeName == 'widememory':
        entrySizeDec = int( entrySize.lstrip('0x') , 16)
        tableRow = {'NAME': '"%s"' % entryName, 'PARENT_NAME': '"%s"' % entryParentName, 'ACCESS': '"%s"' % entryAccess, 'SIZE' : '%d' % entrySizeDec }
      else:
        tableRow = {'NAME': '"%s"' % entryName, 'PARENT_NAME': '"%s"' % entryParentName, 'ACCESS': '"%s"' % entryAccess, 'ARRAYED': '"%s"' % str(entryArrayed), 'SIZE' : '%d' % int(entrySize) }

      if entryName != '' and entryName != '-':
        success = self.createEntry(tableName, tableRow)
  
        if not success:
          initSuccess = False
        if typeName == 'field' and entryCapture != '':
          captureTableName = lb + '_capture'
          captureTableRow = {'NAME': '"%s"' % entryName, 'PARENT_NAME': '"%s"' % entryParentName, 'CAPTURE': '"%s"' % entryCapture }
          success = self.createEntry(captureTableName , captureTableRow )
          if not success:
            initSuccess = False
  
  
    if initSuccess : 
      success = self.createEntry('%s_status' % lb, {'STATUS': '"SUCCESS"' })
    else:
      success = self.createEntry('%s_status' % lb, {'STATUS': '"FALSE"' })


  def parseHtmlInfo(self, lb):
    webUrl = urllib.request.urlopen(common.CSR_DEFINITION_URL + lb + '_csr.html')
  
    # parsing in different block
    inDefinitionBlock = False
    inBitfieldsBlock = False
    inBitfieldBlock = False
    inReferencesBlock = False
    inAttributesBlock = False
    inEnumBlock = False
    # Hierarchy reference name
    refName = ''
    # type, can be register, wideregister, group, memory, widememory
    refType = ''

    # refName to refType dict
    refTypeDict = {}

    # List, formed as (referenced, type)
    csrRefList = []
    # memoryCount
    memoryCount = ''

    # array size 
    arraySize = 1

    # array
    arrayed = False
    # address access
    addressedAccess = ''

    # field name
    fieldName = ''
    # field reference name
    fieldRefName = ''
    # field type
    fieldType = 'field'
    # field access
    fieldAccess = ''

    fieldList = []

    # field linked capture register
    iCapRegister = ''
  
    initSuccess = True
  
    for line in webUrl:
      # iterate each line of html
      line = line.decode("utf-8")
  
      # Looking for version
      '''
      (match, value) = self.htmlExtractTabValue('h2', line)
      if match:
        matchObj = re.match(r'Addressmap Information for \'%s_csr\'.*(ss-tb-.*)' % lb, value)
        if matchObj:
          version = matchObj.group(1)
  
          success = self.createEntry( (lb + common.CSR_REF_VERSION_TABLE_SUFFIX), {common.CSR_REF_VERSION_TABLE_SCHEMA_VERSION: '"%s"' % version})
          if not success:
            initSuccess = False
      '''
  
      # process enum block, skip the block definition
      if inEnumBlock:
        match = self.htmlMatchTab('/csr:enumeration', line)
        if match:
          inEnumBlock= False
        continue
      else:
        match = self.htmlMatchTab('csr:enumeration', line)
        if match:
          inEnumBlock= True
          continue
  
      # parsing references block, skip the block
      if inReferencesBlock:
        # in references block
        # skipping references block, only looking for end of references block
        match = self.htmlMatchTab('/csr:references', line)
        if match:
          inReferencesBlock = False
      else:
        # not in references block
        # looking for start of references block
        match = self.htmlMatchTab('csr:references', line)
        if match:
            inReferencesBlock = True
  
        # parsing definition block
        if inDefinitionBlock:
          # in definition block
          # looking for referenceType
          (match, value) = self.htmlExtractTabValue('csr:referenceType', line)
          if match:
            #self.log.debug('processing type %s' % value)
            refType = value
  
          # looking for referenceName
          (match, value) = self.htmlExtractTabValue('csr:referenceName', line)
          if match:
            #self.log.debug('processing reference %s' % value)
            # Skip 'addressmap'
            refName = value

            fullRefList = refName.split('.')
            if len(fullRefList) > 1:
              parentType = refTypeDict['.'.join(fullRefList[0:-1])]
              if parentType == common.CSR_REF_WIDE_REGISTER:
                refType = common.CSR_REF_SUB_WIDE_REGISTER
              elif parentType == common.CSR_REF_VIRTUAL_WIDE_REGISTER:
                refType = common.CSR_REF_SUB_VIRTUAL_WIDE_REGISTER
              elif parentType == common.CSR_REF_MEMORY:
                refType = common.CSR_REF_VIRTUAL_REGISTER
              elif parentType == common.CSR_REF_WIDE_MEMORY:
                refType = common.CSR_REF_VIRTUAL_WIDE_REGISTER
              elif parentType == common.CSR_REF_ADDRESSMAP:
                pass
              else:
                pass
                #self.log.error('%s has wrong parent type: %s' % (refName, refType))

            refTypeDict[refName] = refType

          # looking for memory count
          (match, value) = self.htmlExtractTabValue('csr:memoryWordCount', line)
          if match:
            #self.log.debug('processing memory count %s' % value)
            # Skip 'addressmap'
            memoryCount = value

          # looking for addressed access
          (match, value) = self.htmlExtractTabValue('csr:addressedAccess', line)
          if match:
            #self.log.debug('processing memory count %s' % value)
            # Skip 'addressmap'
            addressedAccess = value
            #if refType != 'addressmap':
              #if refType == 'memory' or refType == 'widememory': 
                #csrRefList.append((refName.split('.')[-1], refName, refType, addressedAccess, memoryCount, ''))
              #else:
                #csrRefList.append((refName.split('.')[-1], refName, refType, addressedAccess, 1, ''))

          (match, value) = self.htmlExtractTabValue('csr:arrayDimensions', line)
          if match:
            #self.log.debug('processing memory count %s' % value)
            # Skip 'addressmap'
            matchObj = re.match('\[(\d+)\s*-\s*(\d+)\]', value)
            if matchObj:
              arraySize = int(matchObj.group(2)) + 1
              arrayed = True



          # parsing bitfields block
          if inBitfieldsBlock:
            # in bitfields block
            # parsing bitfield block
            if inBitfieldBlock:
              # in bitfield block
              # looking for identifier block
              (match, value) = self.htmlExtractTabValue('csr:identifier', line)
              if match:
                #self.log.debug('processing field %s' % value)
                fieldName = value
                fieldRefName = refName + '.' + fieldName

              (match, value) = self.htmlExtractTabValue('csr:access', line)
              if match:
                fieldAccess = value
              # looking for end of bitfield
              match = self.htmlMatchTab('/csr:bitfield', line)
              if match:
                #csrRefList.append((fieldName, fieldRefName, fieldType, fieldAccess, False, '1', iCapRegister))

                fieldList.append((fieldName, fieldRefName, fieldType, fieldAccess, False, '1', iCapRegister))
                inBitfieldBlock = False


              if inAttributesBlock: 
                #self.log.info(0, 'in field attributes block, line = %s' % line)
                match = self.htmlMatchTab('/csr:fieldAttributes', line)
                if match:
                  inAttributesBlock = False
                (match, value) = self.htmlExtractTabValue('csr:attribute', line)
                if match: 
                  #self.log.info(0, 'in attribute block, line = %s' % line)
                  #self.log.info(0, 'in attribute block, value = %s' % value )
                  matchObj = re.match('icap="(.*)"', value)
                  if matchObj:
                    #self.log.info(0, 'found icap, value = %s' % value )
                    iCapRegister = matchObj.group(1)

              else:
                match = self.htmlMatchTab('csr:fieldAttributes', line)
                if match:
                  inAttributesBlock = True
  
            else:
              # looking for start of bitfield
              match = self.htmlMatchTab('csr:bitfield', line)
              if match:
                inBitfieldBlock = True
                iCapRegister = ''
  
            # looking for end of bitfields
            match = self.htmlMatchTab('/csr:bitfields', line)
            if match:
              inBitfieldsBlock = False
  
          else:
            # looking for start of bitfields
            match = self.htmlMatchTab('csr:bitfields', line)
            if match:
              inBitfieldsBlock = True
  
          # looking for end of definition
          match = self.htmlMatchTab('/csr:definition', line)
          if match:
            inDefinitionBlock = False
            if refType != 'addressmap':
              if refType == 'memory' or refType == 'widememory': 
                csrRefList.append((refName.split('.')[-1], refName, refType, addressedAccess, True, memoryCount, ''))
              else:
                csrRefList.append((refName.split('.')[-1], refName, refType, addressedAccess, arrayed, arraySize , ''))
                while len(fieldList) > 0:
                  csrRefList.append(fieldList[0])
                  fieldList.pop(0)
  
        else:
          # looking for start of definition
          match = self.htmlMatchTab('csr:definition', line)
          if match:
            inDefinitionBlock = True
            arrayed = False
            arraySize = 1
            refName = ''
            refType = ''
  

    return csrRefList;
  
  def csrEntryExists(self, lb, csrEntryName):
    ''' csr entry exists, full csr hierarchy name, 
    including array index([\d]

    Arguments
    ---------

    lb
      lb name

    csrEntryName
      csr entry name, full hierarch, including array index

    Returns
    -------

    exist
      csrEntry exists

    '''

    fullEntryName = ''
    csrEntryList = csrEntryName.split('.')

    for entry in csrEntryList:
      entryName = entry
      entryArrayed = False
      entryArrayIdx = 0
      matchObj = re.match('(.*)\[(\d+)\]', entry)

      if matchObj:
        entryName = matchObj.group(1)
        entryArrayed = True
        entryArrayIdx = int(matchObj.group(2))

      if fullEntryName == '':
        fullEntryName = entryName
      else:
        fullEntryName = fullEntryName + '.' + entryName

      if not self.refDbEntryExists(lb, fullEntryName, entryArrayed, entryArrayIdx):
        return False

    return True

  def refDbEntryExists(self, lb, refName, arrayed=False, arrayIdx = 0):
    ''' reference database entry exists
    not including array index([\d]

    Arguments
    ---------

    lb
      lb name

    refName
      full entry name

    arrayed
      the entry is arrayed

    arrayIdx
      array index 

    Returns
    -------

    exist
      entry exists in reference database

    '''
    self.log.debug('refDbEntryExists lb=%s, refName=%s, arrayed=%s, arrayIdx=%d' % (lb, refName, arrayed, arrayIdx))
    entryFound = False
    refArrayed = str(False)
    refSize = 0
    entryType = ''
    
  
    (parentName, entryName) = self.refNameParse(refName)

    (found, result) = self.getFirstEntryValue('%s_register' % lb, ['"ARRAYED"', '"SIZE"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found :
      entryFound = True
      refArrayed = result[0]
      refSize = result[1]
      entryType = 'register'

    (found, result) = self.getFirstEntryValue('%s_wideregister' % lb, ['"ARRAYED"', '"SIZE"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found :
      entryFound = True
      refArrayed = result[0]
      refSize = result[1]
      entryType = 'wideregister'

    (found, result) = self.getFirstEntryValue('%s_memory' % lb, ['"SIZE"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found:
      entryFound = True
      refArrayed = str(True)
      refSize = result[0]
      entryType = 'memory'
  
    (found, result) = self.getFirstEntryValue('%s_widememory' % lb, ['"SIZE"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found:
      entryFound = True
      refArrayed = str(True)
      refSize = result[0]
      entryType = 'widememory'
  
    (found, result) = self.getFirstEntryValue('%s_group' % lb, ['"ARRAYED"', '"SIZE"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found:
      entryFound = True
      refArrayed = result[0]
      refSize = result[1]
      entryType = 'group'
  
    (found, result) = self.getFirstEntryValue('%s_field' % lb, ['"ARRAYED"', '"SIZE"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found:
      entryFound = True
      refArrayed = result[0]
      refSize = result[1]
      entryType = 'field'

  
    if entryFound:
      if refArrayed == str(True):
        refArrayed = True
      elif refArrayed == str(False):
        refArrayed = False
      else:
        self.error('Wrong ARRAYED column(%s) get from %s_%s' % (refArrayed, lb, entryType))
        return False

      if refArrayed == arrayed:
        if arrayed and (arrayIdx >= refSize):
          return False
        else:
          return True
      else:
        return False
    else:
      return False

  def hierExists(self, lb, hier):
    ''' hierarchy exists

    Arguments
    ---------

    lb
      LB name

    hier
      hierarchyal name

    Returns
    -------

    exist
      hierarchy exists

    '''

    # 
  
    (found, entries) = self.csrRefDb.getEntryValue('%s_register' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'register'
  
 


  def getRefType(self, lb, entryName, parentName):
    ''' Get entry type

    Arguments
    ---------

    lb
      LB name

    entryName
      entry name(NAME column in table)

    parentName
      entry parent name(PARENT_NAME column in table)

    Returns
    -------

    type
      type of entry(register, group, memory...)

    '''

    #self.log.debug( 'getRefType, lb=%s, entryName=%s, parentName=%s' % (lb, entryName, parentName))
    entryName = re.sub('\[\d+\]', '', entryName)
    parentName = re.sub('\[\d+\]', '', parentName)
  
    #self.log.debug( 'entryName is %s, parentName is %s' % (entryName, parentName))
    (found, entries) = self.getEntryValue('%s_register' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'register'
  
    (found, entries) = self.getEntryValue('%s_wideregister' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'wideregister'
  
    (found, entries) = self.getEntryValue('%s_virtual_register' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'virtual_register'
  
    (found, entries) = self.getEntryValue('%s_virtual_wideregister' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'virtual_wideregister'
  
    (found, entries) = self.getEntryValue('%s_memory' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'memory'
  
    (found, entries) = self.getEntryValue('%s_widememory' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'widememory'
  
    (found, entries) = self.getEntryValue('%s_group' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'group'
  
    (found, entries) = self.getEntryValue('%s_field' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'field'

    (found, entries) = self.getEntryValue('%s_virtual_register' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'virtual_register'
  
    (found, entries) = self.getEntryValue('%s_virtual_wideregister' % lb, ['"NAME"'], 'NAME = "%s" and PARENT_NAME = "%s"' % (entryName, parentName))
    if found and len(entries) > 0:
      return 'virtual_wideregister'
 
    # if can not find in any tables, return empty string
    return ''

  def findCsrInfo(self, lb, fullHier):
    ''' Find all register/field/memory/group info

    Arguments
    ---------

    lb
      LB name

    fullHier
      full hierarchy path

    Returns
    -------

    registers with info

    '''


    tableList = []
    tableList.append('%s_register' % lb)
    tableList.append('%s_wideregister' % lb)
    tableList.append('%s_group' % lb)
    tableList.append('%s_field' % lb)
    tableList.append('%s_memory' % lb)
    tableList.append('%s_widememory' % lb)

    regInfo = {}
    hierList = fullHier.split('.')
    parentName = ''
    curRegInfo = regInfo
    for entryName in hierList:
      for table in tableList:
      
        (entryFound, entry) = self.getEntryValue(table, ['"NAME"', '"SIZE"'], 'PARENT_NAME = "%s" and NAME = "%s"' % (parentName, entryName))

        if entryFound:
          if len(entry) > 1:
            self.log.error('Get more than one entry, reference Db contains error')
          else:
            entrySize = entry[0][1]
            curRegInfo[entryName] = {'size': entrySize, 'next': {}}
            curRegInfo = curRegInfo[entryName]['next']
            if  parentName == '':
              parentName = entryName
            else:
              parentName = parentName + '.' + entryName
            break
          
    return regInfo
 
  def findAllCsrInfo(self, lb, sqlRegex='', refType='register'):
    ''' Find all reference information for a lb

    Arguments
    ---------

    lb
      LB name

    sqlRegex
      sql regular expression

    Returns
    -------

    registers with info

    '''

 
    allRefInfo = refInfo()
    resultReference = []

    if refType == 'register':

      (registerFound, registers) = self.getEntryValue( (lb + common.CSR_REF_REGISTER_TABLE_SUFFIX) , ['"PARENT_NAME", "NAME"', '"SIZE"'], 'PARENT_NAME || "." || NAME like "%%%s%%"' % sqlRegex)
      (wideregisterFound, wideregisters) = self.getEntryValue( (lb + common.CSR_REF_WIDE_REGISTER_TABLE_SUFFIX) , ['"PARENT_NAME", "NAME"', '"SIZE"'], 'PARENT_NAME || "." || NAME like "%%%s%%"' % sqlRegex)

      if registerFound:
        resultReference += registers 
      if wideregisterFound:
        resultReference += wideregisters 
    else:
      (fieldFound, fields) = self.getEntryValue( (lb + common.CSR_REF_FIELD_TABLE_SUFFIX), ['"PARENT_NAME", "NAME"', '"SIZE"'], 'PARENT_NAME || "." || NAME like "%%%s%%"' % sqlRegex)
      if fieldFound:
        resultReference += fields
  
    for item in resultReference:

      parentName = item[0]
      entryName = item[1]
      regRefName = self.refNameFormat(parentName, entryName)

      allRefInfo.addInfo(self.findCsrInfo(lb, regRefName ))
 
    self.log.debug('get refInfo ' + str(allRefInfo.getInfo()))
    return allRefInfo.getInfo()

  def formatCsrName(self, refInfo):
    '''
      format csr name based on csr info, including [%d] index, if arrayed

      Arguments
      ---------

      refInfo
        reference information

    '''

    regs = []
    for reg in refInfo:
      if len(refInfo[reg]['next'] ) == 0:
        if refInfo[reg]['size'] == 1:
          regs.append(reg)
        else: 
          for i in range(0, refInfo[reg]['size']):
            regs.append(reg + ('[%d]' % i) )

      else:
        childRegs = self.formatCsrName(refInfo[reg]['next'])

        for childReg in childRegs:
          if refInfo[reg]['size'] == 1:
            regs.append(reg + '.' + childReg)
          else:
            for i in range(0, refInfo[reg]['size']):
              regs.append(reg + ('[%d].' % i) + childReg)
    return regs
      
  def findAllRegister(self, lb, sqlRegex=''):
    regInfo = self.findAllCsrInfo(lb, sqlRegex=sqlRegex, refType='register')
    regList = self.formatCsrName(regInfo)
    return regList

  def findAllField(self, lb, sqlRegex=''):
    fieldInfo = self.findAllCsrInfo(lb, sqlRegex=sqlRegex, refType='field')
    fieldList = self.formatCsrName(fieldInfo)
    return fieldList 


  def findMemInfo(self, lb, memType, memName):
    ''' Find memory info, includes size, virtual registers

    Arguments
    ---------

    lb
      LB name

    memType
      memory type (memory or widememory)

    memName
      memory name 

    Returns
    -------

    memInfo
      dictionary {'size': size, 'register': [register list]}

    '''

    (memoryFound, memoryResults) = self.getEntryValue('%s_%s' % (lb, memType), ['"SIZE"'], 'NAME = "%s" and PARENT_NAME = ""' % (memName))
  
    if memoryFound and len(memoryResults) > 0:
      memSize = memoryResults[0][0]
  
      memInfo = {'size': memSize, 'register': []}
      if memType == 'memory':
        (virtualRegisterFound, virtualRegisterResults) = self.getEntryValue('%s_register' % lb, ['"NAME"'], 'PARENT_NAME = "%s"' % (memName))
        for virtualRegisterResult in virtualRegisterResults:
          memInfo['register'].append(virtualRegisterResult[0])
      else:
        (virtualRegisterFound, virtualRegisterResults) = self.getEntryValue('%s_wideregister' % lb, ['"NAME"'], 'PARENT_NAME = "%s"' % (memName))
        for virtualRegisterResult in virtualRegisterResults:
          memInfo['register'].append(virtualRegisterResult[0])
      return memInfo
  
    else:
      return {'size': 0, 'register': []}
  
  def recursionFindGroupRegisters (self, lb, groupName):
    ''' Find registers under group in recursion way, as there may be groups under a group

    Arguments
    ---------

    lb
      LB name

    groupName
      group name 

    Returns
    -------

    regs
      dict [registers under group]

    '''

    regs = []
  
      
    (groupRegisterFound, groupRegisters) = self.getEntryValue('%s_register' % lb, ['"NAME"'], 'PARENT_NAME = "%s"' % (groupName))
    (groupWideregisterFound, groupWideregisters) = self.getEntryValue('%s_wideregister' % lb, ['"NAME"'], 'PARENT_NAME = "%s"' % ( groupName))
    (groupGroupFound, groupGroups) = self.getEntryValue('%s_group' % lb, ['"NAME"'], 'PARENT_NAME = "%s"' % ( groupName))
    if groupRegisterFound and len(groupRegisters) > 0:
      for item in groupRegisters:
        regs.append(groupName + "." + item[0])
      
    if groupWideregisterFound and len(groupWideregisters) > 0:
      for item in groupWideregisterFound:
        regs.append(groupName + "." + item[0])
  
  
    if groupGroupFound and len(groupGroups) > 0:
      for item in groupGroups:
        regs = regs + self.recursionFindGroupRegisters(lb, groupName + '.' + item[0])
    return regs
  
  def getFields(self, lb, regDefName):
    (fieldFindSuccess, fieldResults) = self.getEntryValue('%s_field' % lb, ['"NAME"'], 'PARENT_NAME = "%s"' % (regDefName) )

    return [field[0] for field in fieldResults]



  def isTypeBaseCsrUnit(self, csrType):
    if csrType in ['register', 'wideregister', 'virtual_register', 'virtual_wideregister']:
      return True
    else:
      return False



  def getBaseCsrUnit(self, lb, fullCsrName):
    hireList = fullCsrName.split('.')
    while len(hireList) > 0:
      entryName = hireList[-1]
      parentName = '.'.join(hireList[0:-1])
      if self.isTypeBaseCsrUnit(self.getRefType(lb, entryName, parentName)):
        return '.'.join(hireList)
      else: 
        hireList.pop(-1)
    return ''

