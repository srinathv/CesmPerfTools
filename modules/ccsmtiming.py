

import logging
from collections import OrderedDict
import gzip
import os.path
# module to 

#1)create dictionaries from ccsm_timing_stats.* files
#2)calculate ratios of categories
#3)print categories and ratios that are +- tolerance of specific category ratio


#1)read in ccsm_timing_stats file

def createDict(filename,dictName):
    timingDict={'name':dictName}    
#test if file name has .gz at end, and if does, open with gzip
    extension = os.path.splitext(filename)[1]
    if (extension == '.gz') :
      lines=gzip.open(filename).readlines()
    else:
      lines=open(filename).readlines()


    i=-1
    for line in lines:
        i=i+1
        if "name" in line:
            nameIndex=i
    timeLines=lines[nameIndex+1:-1]
    for eachLine in timeLines:
        try:
          logging.debug('keys,values' + eachLine.split()[0], eachLine.split()[5])
          timingDict[eachLine.split()[0]]=float(eachLine.split()[5])
        except:
         print "missing"
    return timingDict
    

def calcRatios(dict1,dict2): #dict1 is numerator
    ratioDict={}
    numName=dict1['name']+' time'
    denName=dict2['name']+' time'
    for key,val in dict1.iteritems():
      try:
        ratioDict[key]={'ratio':dict1[key]/dict2[key],numName:dict1[key],denName:dict2[key]}
      except:
        print key, " zero in dict2"
    logging.debug('difference of values array lengths =' + str(len(dict1.keys())-len(dict2.keys())))
    return ratioDict # each category is a ratio of dict1:category:value/dict2:category:value


def beyondTolDict(timeKey,ratioDict,tolerance): #all pairs outside a range of reference
    btDict={}
    for key,val in ratioDict.iteritems():
      if abs(ratioDict[timeKey]['ratio']-ratioDict[key]['ratio']) > tolerance :
        btDict[key]=val
    return btDict

#def DecendRatio(ratioDict,key): #print the items of ratio dict in decending order base on key
#    for key,val in ratioDict.iteritems():

#def moreThanfifty(ratioDict,maxKey):
#    fiftyDict={}
#        for key,val in ratioDict.iteritems():
#            if (ratioDict[maxKey]
#    return fiftyDict
        
