#! /usr/bin/env python

#####
## loop over compilers and compset and threading 
## build and submit if host
## if a step fails, keep going to next combo"

import subprocess
import os,sys,getopt


cesmVersion='cxp'
compsetResDict = {'FIDEAL':'ne16_ne16','FC5AQUAP':'ne16_ne16','FC5':'ne16_ne16','BC5':'ne16_g37'}
nNodesList = [2]
nRanksPerNode = 4
nThreadsPerRank = 48
machine='babbageKnc'
compilerList=['intel','intel14','intel15']
mpiList=['impi','impi4.1.3','impi5.0.up1']
createNewcaseCom='/global/u1/v/vadlaman/cesm1_3_beta09_xeon_phi/scripts/create_newcase'
casesDir='/global/scratch2/sd/vadlaman/cesm_phi_cases'



xmlchangePesBase='./xmlchange -file env_mach_pes.xml -id '
xmlchangeVar=['NTASKS_']
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
        #sys.exit(2)
        pass
  for opt, arg in opts:
      if opt == '-h':
         print howToUse
         sys.exit()
  print 'Exectuting build and run system'
  caseName = '' #initialize

  itTest = False
  if testName:
    isTest = True

  for compset, resolution in compsetResDict.iteritems():
    for nNodes in nNodesList:
      totalNtasks = nNodes * nRanksPerNode
      for compiler in compilerList:
        for mpi in mpiList:
          #build case name
          if isTest:
            caseName = testName + '.'
          
          caseName = machine + '.' + compiler + '.' + mpi
          caseName = caseName + '.' + cesmVersion
          caseName = caseName + '.' + compset + '.' + resolution
          caseName = caseName + '.' + str(nNodes) + 'nodes'
          caseName = caseName + '.' + str(nRanksPerNode) + 'rmp'
          caseName = caseName + '.' + str(nThreadsPerRank) + 'omp'

          cdCommand = 'cd ' + caseName + ' '

          createNewCase = createNewCaseCom + ' -case ' + caseName + ' -res ' + resolution[0] \
                          +  ' -compset ' + compset + ' -mach ' + machine \
                          +  ' -compiler ' + compiler + ' -mpi ' + mpi

          if isTest:
            createNewCase = createNewCase + ' -testname ' + testName

          errorMessage = "the " + caseName + " already exists, failed trying to create new case"
          shellCommand(createNewCase,errorMessage)
          
          commandLine = cdCommand + ' && ./cesm_setup -clean'
          errorMessage = "failed at entering the new case directory or doing ./cesm_setup -clean"
          shellCommand(commandLine,errorMessage)
          
          xmlchangeLines=[]
          xmlchangeLines.append('./xmlchange -file env_run.xml -id STOP_N -val 2')
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
            commandLine = cdCommand + '&&' + commandLine
            errorMessage = "failed at entering the new case directory or doing xmlchange of pes"
            shellCommand(commandLine,errorMessage)

          commandLine = cdCommand + ' && ./cesm_setup -clean && ./cesm_setup'
          errorMessage = "failed at entering  " + caseName + " directory or doing ./cesm_setup "
          shellCommand(commandLine,errorMessage)
          
          commandLine = cdCommand + ' && ' + caseName + '.clean_build'
          errorMessage = "failed at entering  " + caseName + " directory or doing clean_build "
          shellCommand(commandLine,errorMessage)

          commandLine = cdCommand + ' && ' + caseName + '.build'
          errorMessage = "failed at entering " + caseName + "directory or doing build "
          shellCommand(commandLine,errorMessage)

          commandLine = cdCommand + ' && ' + caseName + '.submit'
          errorMessage = "failed at entering " + caseName + "directory or doing submitting "
          shellCommand(commandLine,errorMessage)
       
          caseName = '' # clear the name

if __name__ == "__main__":
   main(sys.argv[1:])

