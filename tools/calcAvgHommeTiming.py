#! /usr/bin/env python

import sys,os
import numpy as np
import pylab as py
sys.path.append('../modules')
try:
  import cesmperftiming as cpt
except:
  print "could not files cesmTimer module"


def main(argv):
  try:
    thisdir = os.path.abspath(".")
    newDir=os.path.join(thisdir,argv[1])
    os.chdir(os.path.dirname(newDir))
  except:
    print "running local"


  primRunList=[]
  numList=[]
  flist=os.listdir(".")
  for fileName in flist:
    if ("HommeTime" in fileName):
      suffix=fileName.split(".")[1]
      if (suffix.isdigit()):
        numList.append(int(suffix))
  #for i in range(1,101):
  for i in numList:
    print i 
    parser=cpt.cesmTimeParser()
    parser.parseFile("HommeTime." + str(i))
    primRunList.append(parser.getDataEntry("prim_run","wallmax"))
    
  print "number of members = ", len(numList)
  primRunArray=np.array(primRunList)
  print "avg = ", np.average(primRunArray)
  print "std = ", np.std(primRunArray)

  try:
    numBins=int(argv[2])
  except:
    numBins=50

  #n,bins,patches=py.hist(primRunArray,bins=50)
  n,bins,patches=py.hist(primRunArray,bins=numBins)
  py.xtitle="prim_run [sec]
  py.show()


if __name__ == "__main__":
   main(sys.argv[0:]) 
   #main()
