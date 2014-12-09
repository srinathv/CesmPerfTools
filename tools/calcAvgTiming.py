#! /usr/bin/env python

import sys,os
import numpy as np
import pylab as py
sys.path.append('../modules')
try:
  import cesmperftiming as cpt
except:
  print "could not files cesmTimer module"


#def main(argv):
def main():
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

  n,bins,patches=py.hist(primRunArray,bins=50)
  py.show()


if __name__ == "__main__":
   #main(sys.argv[1:]) 
   main()
