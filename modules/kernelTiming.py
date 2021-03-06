#! /usr/bin/env python

#need to add method for number of samples
#allow for no identical and log it as attribute


import sys
import os, re
import os.path
import gzip
import getopt
import copy
import numpy as np

class kernelData:
  def __init__(self, name):
    self.totalTimeAr = np.zeros(0)
    self.timePerCallAr= np.zeros(0)
    self.callName = name
    self.isDataSet = False
    self.isIdentical = True

  def setTotalTimeAr(self, totalTime):
    self.totalTimeAr= np.append(self.totalTimeAr,totalTime)

  def setTimePerCallAr(self, timePerCall):
    self.timePerCallAr= np.append(self.timePerCallAr,timePerCall)

  def setCallName(self, name):
    self.callName = name

  def setIsDataSet(self, isDataSet):
    self.isDataSet = isDataSet

  def getTotalTimeAr(self):
      return self.totalTimeAr

  def getTimePerCallAr(self):
    return self.timePerCallAr

  def getCallName(self):
    return self.callName 

  def getIsDataSet(self):
    return self.isDataSet 

  def clearTotalTimeAr(self):
    self.totalTimeAr = np.zeros(0)

  def clearTimePerCallAr(self):
    self.timePerCallAr = np.zeros(0)

  def calcAvgTotalTime(self):
    assert self.isDataSet, "Data for "+ getCallName +" is not set."
    return np.mean(self.getTotalTimeAr())
      
  def calcStdTotalTime(self):
    assert self.isDataSet, "Data for "+ getCallName +" is not set."
    return np.std(self.getTotalTimeAr())
    

  def calNumIterations(self):
    assert self.isDataSet, "Data for "+ getCallName+ " is not set."
    ttAr=self.getTotalTimeAr()[0]
    tPcall=self.getTimePerCallAr()[0]
    return ttAr/tPcall


def getKernelDataObj(myObjects, name):
   for myObj in myObjects:
     if (myObj.getCallName() == name) :
        return myObj
#     else:
#       print name + " is not a call assocaited with an object"


class kernelTimeParser:
  def __init__(self):
    pass
    self.filename = ""
    self.fileSet = False
    self.data = []

  def parseFile(self,filename):
    self.filename = filename
    self.fileSet = True
    self.parse()

  def parse(self,):
    assert (self.fileSet), "Error: filename not set"

    # Parse the file
    extension = os.path.splitext(self.filename)[1]
    if (extension == '.gz') :
      self.fid = gzip.open(self.filename,'r')
    else:
      self.fid = open(self.filename,'r')
    lines = self.fid.readlines()
    self.fid.close()
      

    
   #first figure out how many names. collect backeted quantities until "is identical"
    listOfNames=[]
    for line in lines:
      if " is identical." in line:
        break
      listOfNames.append(re.search(r"\[(\w+)\]", line).group(1))
   #remove duplicates. 
    listOfNames=list(set(listOfNames))
      
   #create kernelData object for each name and set name => list of objects and end of day
    myObjects=[]
    for i, name in enumerate(listOfNames):
      myObjects.append(kernelData(name))
   #read by line
    print 
    for line in lines:
      #get name
      # for each line that has name and total time, set totaltime 
      if " total time " in line:
        callName = re.search(r"\[(\w+)\]", line).group(1)
        time = float(line.split()[-1])
     # find member of myObjects list that has name and append to totalTimeArray
        ttObj=getKernelDataObj(myObjects, callName)
        ttObj.setTotalTimeAr(time)
   # for each line that has name and time per call, set timepercal 
     # find member of myObjects list that has name and append to TimePerCallArray
      if " time per call " in line:
        callName = re.search(r"\[(\w+)\]", line).group(1)
        time = float(line.split()[-1])
     # find member of myObjects list that has name and append to totalTimeArray
        tpcObj=getKernelDataObj(myObjects, callName)
        tpcObj.setTimePerCallAr(time * 10E-6)
    for i,item in enumerate(myObjects):
      myObjects[i].setIsDataSet(True)

    self.data = myObjects

  def getAvgTotalTime(self, name):
    theObj=getKernelDataObj(self.data, name)
    return theObj.calcAvgTotalTime()

  def getStdTotalTime(self, name):
    theObj=getKernelDataObj(self.data, name)
    return theObj.calcStdTotalTime()

  def getNumIterations(self, name):
    theObj=getKernelDataObj(self.data, name)
    return theObj.calNumIterations()
 
  def getCallNames(self):
    callNames=[]
    for obj in self.data:
       callNames.append(obj.getCallName())
    return callNames

if __name__=="__main__":

  myParser = kernelTimeParser()
  myParser.parseFile("../tests/kernelTime.1")

  avg1 = myParser.getAvgTotalTime("kernel_divergence_sphere_v2")
  print avg1
  std2 = myParser.getStdTotalTime("kernel_divergence_sphere_v2")
  print std2
  orgNumIt = myParser.getNumIterations("kernel_divergence_sphere") 
  print orgNumIt



