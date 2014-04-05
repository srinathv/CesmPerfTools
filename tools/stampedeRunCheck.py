#! /usr/bin/env python

#####
## loop over compilers and compset and threading 
## build and submit if host
## if a step fails, keep going to next combo"

import subprocess
import os,sys,getopt


hostDict={'compilers':['intel','intel14'],'mpiRanksPerNode':[16,16]}
micDict={'compilers':['intelmic','intelmic14'],'mpiRanksPerNode':[192,96]}
cesmVersion='c13b7'
compsetList = ['FIDEAL','FC5']
nNodesList = [8]
nthreads = [1 , 2]
resolution=['ne16_ne16']
machine='stampede'
mpi='impi'
#arches=['host','mic']
arches=['host']
quad=False



xmlchangePesBase='./xmlchange -file env_mach_pes.xml -id '
xmlchangeVar=['NTASKS_','NTHRDS_','ROOTPE_']
xmlchangeComponents=['ATM ','LND ','ICE ','OCN ','CPL ','GLC ']
xmlchangeMaxTaskPerNode=' ./xmlchange -file env_mach_pes.xml -id MAX_TASKS_PER_NODE -val '

#ne=16 => 1536 total elements
# thus 1536 elements / 8 nodes is 192 elements per node.  micMpiRanksPerNode[i] * nthreads[j] must = 192 => which i and
# j
#

def shellCommand(command,errorMessage):
  try: 
    print command
    subprocess.check_call(command, stderr=subprocess.STDOUT, shell=True)
  except :
    print errorMessage
    pass

  return

def main(argv):
  howToUse = 'trying this out'
  try:
    opts, args = getopt.getopt(argv,"h")
  except getopt.GetoptError:
        print howToUse
        #sys.exit(2)
        pass
  for opt, arg in opts:
      if opt == '-h':
         print howToUse
         sys.exit()
  print 'Exectuting build and run system'
  caseName = '' #initialize
  for arch in arches:
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
            cdCommand = 'cd ' + caseName + ' '
            createNewCase = './create_newcase -case ' + caseName + ' -res ' + resolution[0] \
                            +  ' -compset ' + compset + ' -mach ' + machine \
                            +  ' -compiler ' + compiler + ' -mpi ' + mpi
            errorMessage = "the " + caseName + " already exists, failed trying to create new case"
            shellCommand(createNewCase,errorMessage)
            
            commandLine = cdCommand + ' && ./cesm_setup -clean'
            errorMessage = "failed at entering the new case directory or doing ./cesm_setup -clean"
            shellCommand(commandLine,errorMessage)
            
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
                xmlchangeLines.append(xmlchangePesBase + var + component + '-val ' + str(value))
            #free up case name for next iteration 
            commandLine = xmlchangeLines[0]
            for line in xmlchangeLines[1:]:
              commandLine = commandLine + ' && ' + line
            if device == 'host':
              commandLine = commandLine + ' &&' + xmlchangeMaxTaskPerNode + '16'
            if device == 'mic':
              commandLine = commandLine + ' &&' + xmlchangeMaxTaskPerNode + '244'
            commandLine = cdCommand + '&&' + commandLine 
            errorMessage = "failed at entering the new case directory or doing xmlchange of pes"
            shellCommand(commandLine,errorMessage)

            commandLine = cdCommand + ' && ./cesm_setup'
            errorMessage = "failed at entering  " + caseName + " directory or doing ./cesm_setup "
            shellCommand(commandLine,errorMessage)
            
            commandLine = cdCommand + ' && ' + caseName + '.clean_build'
            errorMessage = "failed at entering  " + caseName + " directory or doing clean_build "
            shellCommand(commandLine,errorMessage)

            if (device == 'mic') and (quad):
              commandLine = "cp quadrature_mod.F90 " + caseName + "/SourceMods/src.cam ."
              errorMessage = "failed at copying quadrature_mod.F90 into  " + caseName
              shellCommand(commandLine,errorMessage)
              
            commandLine = cdCommand + ' && ' + caseName + '.build'
            errorMessage = "failed at entering " + caseName + "directory or doing build "
            shellCommand(commandLine,errorMessage)

            commandLine = cdCommand + ' && ' + caseName + '.submit'
            if device == 'host':
              errorMessage = "failed at entering " + caseName + "directory or doing submitting "
              shellCommand(commandLine,errorMessage)
         
            caseName = '' # clear the name


if __name__ == "__main__":
   main(sys.argv[1:])




####if MIC then do the run substituions

### for intelmic<14> fix <case>.run file by reading in the file and replacing particular parts
#with open("out.txt", "wt") as fout:
#    with open("Stud.txt", "rt") as fin:
#        for line in fin:
#            fout.write(line.replace('A', 'Orange'))


