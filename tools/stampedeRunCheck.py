#! /usr/bin/env python

#####
## loop over compilers and compset and threading 
## build and submit if host
## if a step fails, keep going to next combo"

import subprocess
import sys

hostDict={'compilers':['intel','intel14'],'mpiRanksPerNode':[16,16]}
micDict={'compilers':['intelmic','intelmic14'],'mpiRanksPerNode':[192,96]}
cesmVersion='c13b7'
compsetList = ['FIDEAL','FC5']
nNodesList = [8]
nthreads = [1 , 2]
resolution=['ne16_n16']
machine='stampede'
mpi='impi'


xmlchangePesBase='./xmlchange -file env_mach_pes.xml -id '
xmlchangeVar=['NTASKS_','NTHRDS_','ROOTPE_']
xmlchangeComponents=['ATM ','LND ','ICE ','OCN ','CPL ','GLC ']
xmlchangeMaxTaskPerNode=' ./xmlchange -file env_mach_pes.xml -id MAX_TASKS_PER_NODE -val '

#ne=16 => 1536 total elements
# thus 1536 elements / 8 nodes is 192 elements per node.  micMpiRanksPerNode[i] * nthreads[j] must = 192 => which i and
# j
#

caseName = '' #initialize
for arch in ['host','mic']:
  device = arch
  if (device == 'host') :
    deviceDict = hostDict
  elif (device == 'mic') :
    deviceDict = micDict
  for nNodes in nNodesList: 
    for i in range(0,len(compsetList)): 
      compset = compsetList[i]
      for j in range(0,len(deviceDict['compilers'])):
        compiler = deviceDict['compilers'][j]
        for indx, rankCount in enumerate(deviceDict['mpiRanksPerNode']):
          #loose logic on position of mpiranks and nthreads
          nRankPerNode = rankCount
          nThreadsPerRank = nthreads[indx] 
          totalNtasks = nNodes * nRankPerNode
          #build case name
          caseName = cesmVersion + '.' + resolution[0]
          caseName = caseName + '.' + str(nNodes) + 'nodes'
          caseName = caseName + '.' + device
          caseName = caseName + '.' + compset
          caseName = caseName + '.' + compiler
          caseName = caseName + '.' + str(nRankPerNode) + 'mpi'
          caseName = caseName + '.' + str(nThreadsPerRank) + 'omp'
          print caseName
          cdCommand = 'cd ' + caseName 
          createNewCase = './create_newcase -case ' + caseName + ' -res ' + resolution[0] \
                          +  ' -compset ' + compset + ' -mach ' + machine \
                          +  ' -compiler ' + compiler + ' -mpi ' + mpi
          try: 
            subprocess.check_call(createNewCase, stderr=subprocess.STDOUT, shell=True)
            print createNewCase
          except ValueError:
            print "the " + caseName + " already exists, failed trying to create new case"

          commandLine = cdCommand + ' && ./cesm_setup -clean'
          try:
            #subprocess.check_call(commandLine, stderr=subprocess.STDOUT, shell=True)
            print commandLine
          except ValueError:
            print "failed at entering the new case directory or doing ./cesm_setup -clean"
          
          xmlchangeLines=[]
          xmlchangeLines.append('./xmlchange -file env_run.xml -id STOP_N -val 5')
          xmlchangeLines.append('./xmlchange -file env_run.xml -id STOP_OPTION -val ndays')
          xmlchangeLines.append('./xmlchange -file env_run.xml -id REST_OPTION -val never')
          xmlchangeLines.append('./xmlchange -file env_run.xml -id TIMER_LEVEL -val 9')
          xmlchangeLines.append('./xmlchange -file env_run.xml -id DOUT_S -val FALSE')
          xmlchangeLines.append('./xmlchange -file env_run.xml -id COMP_RUN_BARRIERS -val TRUE')
          for component in xmlchangeComponents:
            for var in xmlchangeVar:
              if var == 'NTASKS_':
                value = totalNtasks
              elif var == 'NTHRDS_':
                value = nThreadsPerRank
              elif var == 'ROOTPE_':  
                value = 0             
              xmlchangeLines.append(xmlchangePesBase + component + var + str(value))
          #free up case name for next iteration 
          commandLine = xmlchangeLines[0]
          for line in xmlchangeLines[1:]:
            commandLine = commandLine + ' && ' + line
          if device == 'host':
            commandLine = commandLine + ' &&' + xmlchangeMaxTaskPerNode + '16'
          if device == 'mic':
            commandLine = commandLine + ' &&' + xmlchangeMaxTaskPerNode + '244'
          commandLine = cdCommand + commandLine 
          try:
            subprocess.check_call(commandLine, stderr=subprocess.STDOUT, shell=True)
            print commandLine
          except :
            print "failed at entering the new case directory or doing xmlchange of pes"

          commandLine = cdCommand + ' && ./cesm_setup'
          try:
            subprocess.check_call(commandLine, stderr=subprocess.STDOUT, shell=True)
            print commandLine
          except :
            print "failed at entering  " + caseName + " directory or doing ./cesm_setup "
            pass
          
          commandLine = cdCommand + ' && ' + caseName + '.clean_build'
          try:
            subprocess.check_call(commandLine, stderr=subprocess.STDOUT, shell=True)
            print commandLine
          except :
            print "failed at entering  " + caseName + " directory or doing clean_build "
            pass

          commandLine = cdCommand + ' && ' + caseName + '.build'
          try:
            subprocess.check_call(commandLine, stderr=subprocess.STDOUT, shell=True)
            print commandLine
          except:
            print "failed at entering " + caseName + "directory or doing build "
            pass
          commandLine = cdCommand + ' && ' + caseName + '.submit'
          if device == 'host':
            try:
              subprocess.check_call(commandLine, stderr=subprocess.STDOUT, shell=True)
              print commandLine
            except:
              print "failed at entering " + caseName + "directory or doing submitting "
              pass            
          caseName = '' # clear the name







####if MIC then do the run substituions

### for intelmic<14> fix <case>.run file by reading in the file and replacing particular parts
#with open("out.txt", "wt") as fout:
#    with open("Stud.txt", "rt") as fin:
#        for line in fin:
#            fout.write(line.replace('A', 'Orange'))


