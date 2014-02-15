#! /usr/bin/python

from ccsmtiming import *
import numpy as np
import logging


#MAIL content from Ilene (1/28/2014):
#The atmospheric component takes 1776 sec.
#cam_run2 takes 181 sec.  This is mostly the "ac_physics" (after coupling), which takes 113 sec and the transfer of data from physics data structures to dynamics data structures (p_d_coupling), which takes about 17 sec.
#cam_run1 takes 364 sec. This is mostly the "bc_physics" (before coupling), which takes 332 seconds. The d_p_coupling takes about 9 sec.
#
#Roughly we can estimate that the time in physics is cam_run1+cam_run2=364+181 sec=545 sec. This is about 30% of the 1776 sec that the atmospheric component takes.
#
#The HOMME stuff is in camrun3, 1099 sec so that is about 62% of the time in the atmospheric component.
#
#For this case with the tracers from CAM5 physics, there is more time spent in tracer advection in HOMME than in the regular dynamics. prim_advance_exp (regular dynamics) takes 428 seconds, prim_advect_tracers_remap_rk2 takes 662 sec.


kncDict=createDict("stampede/timinglogs/ccsm_timing_stats.140113-110333_FC5_ne16ne16_comp13_optO0.gz",'knc')

print "\n"
print "KNC run on Stampede "
print "8 nodes, 8 mpi ranks per node "
print "24 threads per mpi rank "
print "intel/13.1.1.163 "
print "impi/4.1.1.036 "
print "CESM 1.3.beta01 "
print "ne16_n16 FC5"
print "-O0 optimization"
print "\n"

print "Following times are wall max of all 64 mpi ranks in seconds. \n"
print " kncDict['DRIVER_ATM_RUN'] = ", kncDict['DRIVER_ATM_RUN']
print " kncDict['DRIVER_RUN_LOOP'] = ", kncDict['DRIVER_RUN_LOOP']
print " \n"
print " kncDict['CAM_run2'] = ", kncDict['CAM_run2']
print " kncDict['ac_physics'] = ", kncDict['ac_physics']
print " kncDict['p_d_coupling'] = ", kncDict['p_d_coupling']
print " \n"
print " kncDict['CAM_run1'] = ", kncDict['CAM_run1']
print " kncDict['bc_physics'] = ", kncDict['bc_physics']
print " kncDict['d_p_coupling'] = ", kncDict['d_p_coupling']
print " \n"
print " kncDict['CAM_run3'] = ", kncDict['CAM_run3']
print " kncDict['prim_advance_exp'] = ", kncDict['prim_advance_exp']
print " kncDict['compute_and_apply_rhs'] = ", kncDict['compute_and_apply_rhs']
print " kncDict['prim_advec_tracers_remap_rk2'] = ", kncDict['prim_advec_tracers_remap_rk2']
print " kncDict['euler_step'] = ", kncDict['euler_step']
print " kncDict['advance_hypervis_dp'] = ", kncDict['advance_hypervis_dp']

print " \n"

print" CAM physics percentage (of ATM) is ( CAM_run1 + CAM_run2)/ DRIVER_ATM_RUN * 100  = ", (kncDict['CAM_run1'] + kncDict['CAM_run2'])/kncDict['DRIVER_ATM_RUN'] * 100.
print " Dynamics percentage (of ATM) is CAM_run3 / DRIVER_ATM_RUN * 100 = ", (kncDict['CAM_run3'])/kncDict['DRIVER_ATM_RUN'] * 100.
print " \n"

print" CAM physics percentage Total is ( CAM_run1 + CAM_run2)/ DRIVER_RUN_LOOP * 100  = ", (kncDict['CAM_run1'] + kncDict['CAM_run2'])/kncDict['DRIVER_RUN_LOOP'] * 100.
print" Dynamics percentage of total run is CAM_run3 / DRIVER_RUN_LOOP * 100 = ", (kncDict['CAM_run3'])/kncDict['DRIVER_RUN_LOOP'] * 100.
#print " \n"




#print " kncDict[''] = ", kncDict['']

#kncHostRatioDict=calcRatios(kncDict,hostDict)
#logging.debug(kncHostRatioDict.keys())

#biggerThan10=beyondTolDict('DRIVER_RUN_LOOP',kncHostRatioDict,10)
#print "timers with larger than a 10 ratio = \n",biggerThan10
#
#print "\n"
#
#print "these are knc timed categories that are more than 50% of the total run time \n"
#for key,val in kncHostRatioDict.iteritems():
#   if (kncHostRatioDict[key]['knc time']/kncHostRatioDict['DRIVER_RUN_LOOP']['knc time']) > .5:
#     print key , kncHostRatioDict[key]
