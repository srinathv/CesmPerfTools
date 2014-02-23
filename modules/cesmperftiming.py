
import sys
import os
import os.path
import gzip
import getopt
import copy
import numpy as np

class ParseData:
  def __init__(self):
    self.numMpiProcs = -1
    self.numOmpThreads = -1
    self.numRows = -1
    self.numCols = -1
    self.routineNames = []
    self.colHeaders = []
    self.dataTable = None
    self.dataSet = False

  def setNumMpiProcs(self,numMpiProcs):
    self.numMpiProcs = numMpiProcs

  def setNumOmpThreads(self,numOmpThreads):
    self.numOmpThreads = numOmpThreads

  def getNumMpiProcs(self):
    return self.numMpiProcs

  def getNumOmpThreads(self):
    return self.numOmpThreads

  def setNumRowsCols(self,numRows,numCols):
    self.numRows = numRows
    self.numCols = numCols
    self.dataTable = np.zeros((numRows,numCols))
    self.dataTable[:,:] = -1

  def setData(self,dataBlock,subroutineNames,columnHeaders):
    for iRow in range(len(dataBlock)):
      self.dataTable[iRow,0] = dataBlock[iRow][3]
      self.dataTable[iRow,1] = dataBlock[iRow][4]
      self.dataTable[iRow,2] = dataBlock[iRow][5]
      self.dataTable[iRow,3] = dataBlock[iRow][6]

    self.routineNames = subroutineNames[:]
    self.colHeaders.append(columnHeaders[3])
    self.colHeaders.append(columnHeaders[4])
    self.colHeaders.append(columnHeaders[5])
    self.colHeaders.append(columnHeaders[6])
    self.dataSet = True

  def getData(self):
    assert (self.dataSet), "Error: Data not set"
    return self.dataTable, self.routineNames, self.colHeaders

  def getDataEntry(self,rowKey,colKey):

    # find the index of the rowKey in rowHeaders
    try:
      rowIndex = self.routineNames.index(rowKey)
    except ValueError:
      print ""
      print "Routine name ", rowKey, " not found, valid values are: ", self.routineNames[:]
      return 

    try:
      colIndex = self.colHeaders.index(colKey)
    except ValueError:
      print ""
      print "Column header ", colKey, " not found, valid values are: ", self.colHeaders[:]
      return 

    return self.dataTable[rowIndex, colIndex]

  def getDataCol(self,colKey):

    try:
      colIndex = self.colHeaders.index(colKey)
    except ValueError:
      print ""
      print "Column header ", colKey, " not found, valid values are: ", self.colHeaders[:]
      return 

    return self.dataTable[:, colIndex]

  def getDataRow(self,rowKey):

    # find the index of the rowKey in rowHeaders
    try:
      rowIndex = self.routineNames.index(rowKey)
    except ValueError:
      print ""
      print "Routine name ", rowKey, " not found, valid values are: ", self.routineNames[:]
      return 

    return self.dataTable[rowIndex, :]

  def getRoutineNames(self,):
    return self.routineNames

  def getColHeaders(self,):
    return self.colHeaders

class cesmTimeParser:
  def __init__(self):
    pass
    self.filename = ""
    self.fileSet = False
    self.data = ParseData()

  def parseFile(self,filename):
    self.filename = filename
    self.fileSet = True
    self.parse()

  def printRunInfo(self,):
    assert (self.fileSet), "Error: filename not set"
    print "The run for file", self.filename, "used", self.getNumMpiProcs() , "MPI processes and ", self.getNumOmpThreads(), "threads"
    print "  and took", cesmTimeParser.getDataEntry("Total","wallmax"), "seconds"

  def parse(self,):
    assert (self.fileSet), "Error: filename not set"

    # Parse the file
    extension = os.path.splitext(self.filename)[1]
    if (extension == '.gz') :
      #lines=gzip.open(self.filename,'r')
      self.fid = gzip.open(self.filename,'r')
    else:
      self.fid = open(self.filename,'r')


    # Burn a line
    self.fid.readline()

    # Read the Global statistics line 
    globLine = self.fid.readline().split()

    self.setNumMpiProcs(int(globLine[4]))

    # Burn three lines
    self.fid.readline()
    self.fid.readline()
    self.fid.readline()

    colHeaders = self.fid.readline().split()

    # There are 22 rows in the summary data
    #numRows = 22
    rowData = []
    emptyLine = False
    numRows = 0
    while (not emptyLine):
      inLine = self.fid.readline()
      #if not inLine.strip():
      if inLine.strip():
        rowData.append(inLine.split())
        numRows += 1
      else:
        emptyLine = True

    # Done reading the file close it down
    self.fid.close()

    # Deal with the "(proc", "thrd", and ")" fields
    #   The following is ugly, but cannot be helped 
    ignoreIndices1 = []

    ignoreIndices1.append(colHeaders.index("(proc"))
    ignoreIndices1.append(colHeaders.index("thrd"))
    ignoreIndices1.append(colHeaders.index(")"))

    # Need to do delete these in backwards order to not change the indices
    colHeaders.pop(ignoreIndices1[2])
    colHeaders.pop(ignoreIndices1[1])
    colHeaders.pop(ignoreIndices1[0])


    ignoreIndices2 = []
    ignoreIndices2.append(colHeaders.index("(proc"))
    ignoreIndices2.append(colHeaders.index("thrd"))
    ignoreIndices2.append(colHeaders.index(")"))


    # Need to do delete these in backwards order to not change the indices
    colHeaders.pop(ignoreIndices2[2])
    colHeaders.pop(ignoreIndices2[1])
    colHeaders.pop(ignoreIndices2[0])

    #print colHeaders

    for row in rowData:
      for iPop in reversed(ignoreIndices1):
        row.pop(iPop)
      for iPop in reversed(ignoreIndices2):
        row.pop(iPop)

    subNames = []
    maxNumThreads = -1
    for row in rowData:
      subNames.append(row[0])
      if int(row[2]) > maxNumThreads:
        maxNumThreads = int(row[2])

    numOmpThreads = maxNumThreads/self.getNumMpiProcs()
    #print subNames
    #print maxNumThreads

    self.data.setNumOmpThreads(numOmpThreads)

    numCols = len(rowData[0]) - 3
    self.data.setNumRowsCols(numRows,numCols)
    self.data.setData(rowData,subNames,colHeaders)

  def getDataTable(self,):
    # Return the data
    return self.data.getData()

  def getDataEntry(self,rowKey,colKey):
    # Return the data
    return self.data.getDataEntry(rowKey,colKey)

  def getDataCol(self,colKey):
    # Return the data
    return self.data.getDataCol(colKey)

  def getDataRow(self,rowKey):
    # Return the data
    return self.data.getDataRow(rowKey)

  def getRoutineNames(self,):
    return self.data.getRoutineNames()

  def getColHeaders(self,):
    return self.data.getColHeaders()

  def setNumMpiProcs(self,numMpiProcs):
    self.data.setNumMpiProcs(numMpiProcs)

  def setNumOmpThreads(self,numOmpThreads):
    self.data.setNumOmpThreads(numOmpThreads)

  def getNumMpiProcs(self,):
    return self.data.getNumMpiProcs()

  def getNumOmpThreads(self,):
    return self.data.getNumOmpThreads()

if __name__=="__main__":

  myParser = cesmTimeParser()
  #myParser.parseFile("HommeTime")
  myParser.parseFile("../tests/ccsm_timing_stats.140211-005635.gz")

  wallMax = cesmTimeParser.getDataCol("wallmax")
  subNames = cesmTimeParser.getRoutineNames()

  #myParser.printRunInfo()

  for i in range(len(wallMax)): 
    print "Routine", subNames[i], "took", wallMax[i], "s"

  print "Wallmax time for DRIVER_INIT=", cesmTimeParser.getDataEntry("DRIVER_INIT","wallmax")
