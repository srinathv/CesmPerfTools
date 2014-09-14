#! /usr/bin/env python

#####
## loop over compilers and compset and threading 
## build and submit if host
## if a step fails, keep going to next combo"

import subprocess
import os,sys,getopt


testName=''
cesmVersion='cxp'
compsetResDict = {'FC5':'ne16_ne16'}
nNodesList = [2]
#nRanksPerNode = 4
#nThreadsPerRank = 48

#creating a base list for mpi rank order 
#neBaselist=[1,2,4,8,12,16,24,48,96,192] # mpi * threads = 192
fullList=[1,2,4,8,16,32] # mpi * threads = 32
#make lsit of tuples
#ranksThreadsList=zip(neBaselist,neBaselist[::-1])
ranksThreadsList=zip(fullList,fullList[::-1])


machine='babbage'
compilerList=['intel15']
mpiList=['impi5.0.up1']
createNewCaseCom='/global/u1/v/vadlaman/cesm1_3_beta09_xeon_phi/scripts/create_newcase'
#createNewCaseCom='/Users/srinathv/Repos/cesm1_3_beta09_xeon_phi/scripts/create_newcase'
casesDir='/global/scratch2/sd/vadlaman/cesm_phi_cases'
#casesDir='/Users/srinathv/Temp'


#change key word from nodes to cards if Knc in machine name

if ('Knc' in machine):
  nodeType='cards'
else:
  nodeType='nodes'

#from Sheri's script
#    ./xmlchange -file env_run.xml -id STOP_N -val 5
#    ./xmlchange -file env_run.xml -id STOP_OPTION -val ndays
#    ./xmlchange -file env_run.xml -id REST_OPTION -val never
#    ./xmlchange -file env_run.xml -id TIMER_LEVEL -val 9
#    ./xmlchange -file env_run.xml -id DOUT_S -val FALSE
#    ./xmlchange -file env_run.xml -id COMP_RUN_BARRIERS -val TRUE


xmlchangePesBase=' ./xmlchange -file env_mach_pes.xml -id '
xmlchangeRunBase=' ./xmlchange -file env_run.xml -id '
xmlchangeVar=['NTASKS_','NTHRDS_']
xmlchangeComponents=['ATM ','LND ','ICE ','OCN ','CPL ','GLC ','ROF ','WAV ']

def shellCommand(command,errorMessage):
#command initiated where this script is ran
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
        sys.exit(2)
        pass
  for opt, arg in opts:
      if opt == '-h':
         print howToUse
         sys.exit()
  print 'Exectuting build and run system'
  caseName = '' #initialize

  isTest = False
  if testName:
    isTest = True

  for compset, resolution in compsetResDict.iteritems():
    for nNodes in nNodesList:
      for compiler in compilerList:
        for mpi in mpiList:
          for ranksThreads in ranksThreadsList:
            totalNtasks = nNodes * ranksThreads[0]
            #build case name
            if isTest:
              caseName = testName + '.'
            
            caseName = machine + '.' + compiler + '.' + mpi
            caseName = caseName + '.' + cesmVersion
            caseName = caseName + '.' + compset + '.' + resolution
            caseName = caseName + '.' + str(nNodes) + nodeType
            caseName = caseName + '.' + str(ranksThreads[0]) + 'rpm'
            caseName = caseName + '.' + str(ranksThreads[1]) + 'omp'

            cdCommand = 'cd ' + casesDir + '/' + caseName + ' '

            createNewCase = createNewCaseCom + ' -case ' + caseName + ' -res ' + resolution \
                            +  ' -compset ' + compset + ' -mach ' + machine \
                            +  ' -compiler ' + compiler + ' -mpi ' + mpi

            if isTest:
              createNewCase = createNewCase + ' -testname ' + testName

            errorMessage = "the " + caseName + " already exists, failed trying to create new case"
            shellCommand(createNewCase,errorMessage)
            
            commandLine = cdCommand + ' && ./cesm_setup -clean'
            errorMessage = "failed at entering the new case directory or doing ./cesm_setup -clean"
            shellCommand(commandLine,errorMessage)
            
  #create list of xml file changes
  ## start with env_run.xml
            xmlchangeLines=[]
            xmlchangeLines.append(' ./xmlchange -file env_run.xml -id STOP_N -val 2')
            xmlchangeLines.append(' ./xmlchange -file env_run.xml -id STOP_OPTION -val ndays')
            xmlchangeLines.append(' ./xmlchange -file env_run.xml -id REST_OPTION -val never')
            xmlchangeLines.append(' ./xmlchange -file env_run.xml -id TIMER_LEVEL -val 9')
            xmlchangeLines.append(' ./xmlchange -file env_run.xml -id DOUT_S -val FALSE')
           # xmlchangeLines.append(' ./xmlchange -file env_run.xml -id COMP_RUN_BARRIERS -val TRUE')
  ## now change the env_mach_pes.xml
            for component in xmlchangeComponents:
              for var in xmlchangeVar:
                if var == 'NTASKS_':
                  value = totalNtasks
                elif var == 'NTHRDS_':
                  value = ranksThreads[1]
                elif var == 'ROOTPE_':
                  value = 0
                xmlchangeLines.append(xmlchangePesBase + var + component + '-val ' + str(value))

  ## do the xml changes
            for line in xmlchangeLines:
              commandLine = cdCommand + '&&' + line
              errorMessage = "failed at entering the new case directory or doing xmlchange of pes"
              shellCommand(commandLine,errorMessage)



  #clean build , build and submit stage

            commandLine = cdCommand + ' && ./cesm_setup -clean && ./cesm_setup'
            errorMessage = "failed at entering  " + caseName + " directory or doing ./cesm_setup "
            shellCommand(commandLine,errorMessage)
            
            commandLine = cdCommand + ' && ' + './' + caseName + '.clean_build'
            errorMessage = "failed at entering  " + caseName + " directory or doing clean_build "
            shellCommand(commandLine,errorMessage)

            commandLine = cdCommand + ' && ' + './' + caseName + '.build'
            errorMessage = "failed at entering " + caseName + "directory or doing build "
            shellCommand(commandLine,errorMessage)

            commandLine = cdCommand + ' && ' + './' + caseName + '.submit'
            errorMessage = "failed at entering " + caseName + "directory or doing submitting "
            shellCommand(commandLine,errorMessage)

            caseName = '' # clear the name

if __name__ == "__main__":
   main(sys.argv[1:])

