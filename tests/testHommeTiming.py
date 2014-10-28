#! /usr/bin/env python

import sys
import numpy as np
sys.path.append('../modules')
try:
  import cesmperftiming as cpt
except:
  print "could not files cesmTimer module"


#def main(argv):
def main():
  file15 = "HommeTime.1"
  file16 = "HommeTime.2"

  fifteenRanks = cpt.cesmTimeParser()
  sixteenRanks = cpt.cesmTimeParser()
  fifteenRanks.parseFile(file15)
  sixteenRanks.parseFile(file16)

  wallMax15 = fifteenRanks.getDataCol("wallmax")
  wallMax16 = sixteenRanks.getDataCol("wallmax")
  subNames = fifteenRanks.getRoutineNames()

#  fifteenRanks.printRunInfo()

  for i in range(len(wallMax15)):
    print " HommeTime.1", subNames[i], "took", wallMax15[i], "s"

  primRunList=[]
  for i in range(1,3):
    print i 
    parser=cpt.cesmTimeParser()
    parser.parseFile("HommeTime." + str(i))
    primRunList.append(parser.getDataEntry("prim_run","wallmax"))
    
  primRunArray=np.array(primRunList)
  print "avg = ", np.average(primRunArray)
  print "std = ", np.std(primRunArray)



if __name__ == "__main__":
   #main(sys.argv[1:]) 
   main()
