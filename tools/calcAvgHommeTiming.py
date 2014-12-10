#! /usr/bin/env python

import sys,os
import numpy as np
import matplotlib.pyplot as py
sys.path.append('../modules')
try:
  import cesmperftiming as cpt
except:
  print "could not files cesmTimer module"


def main(argv):
  thisPath = os.path.abspath(".")
  try:
    newPath=os.path.join(thisPath,argv[1])
    os.chdir(os.path.dirname(newPath))
    thisPath=newPath
  except:
    print "running local"

  thisDir=thisPath.split("/")[-2]

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
  fig1=py.figure(1)
  ax = fig1.add_subplot(1,1,1,)
  n,bins,patches=ax.hist(primRunArray,bins=numBins)
  py.xlabel("prim_run [sec]")
  py.ylabel("Number of Homme trials")
  py.title(thisDir + "\n NE=3, 1 mpi rank at full device thread use\n Gaussian like")
  py.show()


if __name__ == "__main__":
   main(sys.argv[0:]) 
   #main()
