#! /usr/bin/env python

import sys
sys.path.append('../modules')
try:
  import cesmTimer as ct
except:
  print "could not files cesmTimer module"


#def main(argv):
def main():
  file15 = "ccsm_timing_stats-stampede-15x2x8.13.gz"
  file16 = "ccsm_timing_stats-stampede-16x2x8.13.gz"

  fifteenRanks = ct.cesmTimeParser()
  sixteenRanks = ct.cesmTimeParser()
  fifteenRanks.parseFile(file15)
  sixteenRanks.parseFile(file16)

  wallMax15 = fifteenRanks.getDataCol("wallmax")
  wallMax16 = sixteenRanks.getDataCol("wallmax")
  subNames = fifteenRanks.getRoutineNames()

#  fifteenRanks.printRunInfo()

  for i in range(len(wallMax15)):
    print "15 Rank per node Routine", subNames[i], "took", wallMax15[i], "s"

  print "Wallmax ratio [15mpiranks/16mpiranks] time for DRIVER_INIT=", (fifteenRanks.getDataEntry("DRIVER_INIT","wallmax")/sixteenRanks.getDataEntry("DRIVER_INIT","wallmax"))
  print "Wallmax ratio [15mpiranks/16mpiranks] time for DRIVER_RUN_LOOP=", (fifteenRanks.getDataEntry("DRIVER_RUN_LOOP","wallmax")/sixteenRanks.getDataEntry("DRIVER_RUN_LOOP","wallmax"))


if __name__ == "__main__":
   #main(sys.argv[1:]) 
   main()
