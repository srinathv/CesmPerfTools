#! /usr/bin/python

from ccsmtiming import *
import numpy as np
import logging

## assuming loglevel is bound to the string value obtained from the
## command line argument. Convert to upper case to allow the user to
## specify --log=DEBUG or --log=debug
#numeric_level = getattr(logging, loglevel.upper(), None)
#if not isinstance(numeric_level, int):
#    raise ValueError('Invalid log level: %s' % loglevel)
#logging.basicConfig(level=numeric_level)

hostDict=createDict("stampede/fci.host.16omp.1mpi.8nodes/ccsm_timing_stats.130910-035701",'host')
kncDict=createDict("stampede/fcideal.mic.24omp.8mpi.O3/ccsm_timing_stats.131209-220102",'knc')

print "\n"

kncHostRatioDict=calcRatios(kncDict,hostDict)
logging.debug(kncHostRatioDict.keys())

biggerThan10=beyondTolDict('DRIVER_RUN_LOOP',kncHostRatioDict,10)
print "timers with larger than a 10 ratio = \n",biggerThan10

print "\n"

print "these are knc timed categories that are more than 50% of the total run time \n"
for key,val in kncHostRatioDict.iteritems():
   if (kncHostRatioDict[key]['knc time']/kncHostRatioDict['DRIVER_RUN_LOOP']['knc time']) > .5:
     print key , kncHostRatioDict[key]
