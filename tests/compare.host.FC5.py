#! /usr/bin/python

from ccsmtiming import *
import numpy as np
import logging
import matplotlib.pyplot as plt


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


host13Dict=createDict("stampede/cesm1307.baseline.host.1omp.16mpi/ccsm_timing_stats_13intel_opt_default",'host13')
host14Dict=createDict("stampede/cesm1307.baseline.host.1omp.16mpi/ccsm_timing_stats_14intel_opt_default.gz",'host14')

print "\n"
print "Sandybridge run on Stampede "
print "8 nodes, 16 mpi ranks per node "
print "1 threads per mpi rank "
print "compilers: "
print "intel/13.1.1.163 "
print "impi/4.1.1.036 "
print "and"
print "intel/14.0.1.106"
print "impi/4.1.2.040"
print "CESM 1.3.beta07 "
print "ne16_n16 FC5"
print "default optimization"
print "\n"

ratio1413Dict=calcRatios(host14Dict,host13Dict)

ratioList=[ratio1413Dict['DRIVER_RUN_LOOP']['ratio'],ratio1413Dict['DRIVER_ATM_RUN']['ratio'], ratio1413Dict['CAM_run1']['ratio'], ratio1413Dict['CAM_run2']['ratio'], ratio1413Dict['CAM_run3']['ratio']]

cam3RatioList=[ratio1413Dict['prim_advance_exp']['ratio'],ratio1413Dict['compute_and_apply_rhs']['ratio'],ratio1413Dict['advance_hypervis_dp']['ratio'],ratio1413Dict['prim_advec_tracers_remap_rk2']['ratio'],ratio1413Dict['vertical_remap']['ratio']]
#print ratioList

ratioArray=np.array(ratioList)
cam3RatioArray=np.array(cam3RatioList)

outerTimedGroups=['DRIVER_RUN_LOOP','DRIVER_ATM_RUN','CAM_run1','CAM_run2','CAM_run3']
cam3TimedGroups=['prim_advance_exp','compute_and_apply_rhs','advance_hypervis_dp','prim_advec_tracers_remap_rk2','vertical_remap']

#pos = np.arange(int(np.size(snb1kTime))/2) +.5    # the bar centers on the x axis
pos = np.arange(int(np.size(ratioList)))    # the bar centers on the x axis
width = 0.35

plt.rc(('xtick','ytick','axes'), labelsize=16.0)


def autolabelRel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        if (height == 0):
          print "skiping top label b/c zero"
        else:
          plt.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%.2f'%float(height),
                ha='center', va='bottom')



plt.figure(1)
ratioBars = plt.bar(pos, ratioArray, width, color='b')

plt.ylabel('Normalized time')
plt.xlabel('Timed categroies')
plt.xticks(pos+width, outerTimedGroups)
#plt.legend((ratioBars),('Sandybridge'))
plt.title('SNB on Stampede FC5, ne16_ne16 \n' +
          '(intel/14.0.1.106,impi/4.1.2.040)/(intel/13.1.1.163,impi/4.1.1.036)' +
          '\n CESM 1_3_beta07 \n 8 nodes, 16 mpi ranks per node, 1 thread per rank ',fontsize=12.)
autolabelRel(ratioBars)

pos = np.arange(int(np.size(cam3RatioArray))) 
plt.figure(2)
cam3RatioBars = plt.bar(pos, cam3RatioArray, width, color='g')

plt.ylabel('Normalized time')
plt.xlabel('Timed categroies')
plt.xticks(pos+width, cam3TimedGroups)
#plt.legend((ratioBars),('Sandybridge'))
plt.title('SNB on Stampede FC5, ne16_ne16 \n (intel/14.0.1.106,impi/4.1.2.040)/(intel/13.1.1.163,impi/4.1.1.036) \n CESM 1_3_beta07 \n 8 nodes, 16 mpi ranks per node, 1 thread per rank ',fontsize=12.)
autolabelRel(cam3RatioBars)

plt.show()


