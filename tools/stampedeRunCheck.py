#! /usr/bin/env python

#####
## loop over compilers and compset and threading 
## build and submit if host
## if a step fails, keep going to next combo"

import subprocess
import os,sys,getopt


#hostDict={'compilers':['intel','intel14'],'mpiRanksPerNode':[1,2,4,8,16]}
#hostDict={'compilers':['intel'],'mpiRanksPerNode':[1,2]}
#hostDict={'compilers':['intel'],'mpiRanksPerNode':[4,8,16,1,2,4,8,16]}
hostDict={'compilers':['intel'],'mpiRanksPerNode':[16]}
#hostDict={'compilers':['intel','intel14'],'mpiRanksPerNode':[16,16]}
#micDict={'compilers':['intelmic','intelmic14'],'mpiRanksPerNode':[60,48,30,8]}
cesmVersion='cesm1_2_2'
compsetList = ['FC5AQUAP']
#compsetList = ['FIDEAL','FC5']
#testList = ['PFS'] #-testname PFS
#nNodesList = [1]
nNodesList = [72,144]
#nthreads = [8,4,2,16,8,4,2,1]
nthreads = [2]
#nthreads = [32,16]
#resolution=['ne16_ne16']
resolution=['ne120_ne120']
machine='stampede'
mpi='impi'
testName='PFS'
#arches=['host','mic']
arches=['host']
quad=False



xmlchangePesBase='./xmlchange -file env_mach_pes.xml -id '
xmlchangeVar=['NTASKS_','NTHRDS_','ROOTPE_']
xmlchangeComponents=['ATM ','LND ','ICE ','OCN ','CPL ','GLC ','ROF ','WAV ']
xmlchangeMaxTaskPerNode=' ./xmlchange -file env_mach_pes.xml -id MAX_TASKS_PER_NODE -val '

#ne=16 => 1536 total elements
# thus 1536 elements / 8 nodes is 192 elements per node.  micMpiRanksPerNode[i] * nthreads[j] must = 192 => which i and
# j
#

def shellCommand(command,errorMessage):
#command initiated where this script is ran
  try: 
    print command
    subprocess.check_call(command, stderr=subprocess.STDOUT, shell=True)
  except :
    print errorMessage
    pass
  return


def fixCaseRunFile(caseName, device, nThreadsPerRank, nRanksPerNode, nNodes, time='01:30:00'):
  inputFileName = caseName + "/" + caseName + ".run"
  inputFile = open(inputFileName,'r')
  outputFileName = caseName + "/" + caseName + ".run.swap"
  outputFile = open(outputFileName,'w')
  for line in inputFile.xreadlines():
    outline = line
    ompLine = ''
    if "#SBATCH -N" in line :
     outline = '#SBATCH -N ' + str(nNodes) + "\n"

    if device == 'host':
      ompLine = "setenv OMP_NUM_THHREADS " + str(nThreadsPerRank) + "\n"
      ompLine = ompLine + "setenv OMP_STACKSIZE 500M \n"
      if "#SBATCH -n" in line :
        outline = '#SBATCH -n ' + str(nRanksPerNode * nNodes)  + "\n"
      if "setenv SLURM_NPROCS" in line :
        outline = 'setenv SLURM_NPROCS ' + str(nRanksPerNode * nNodes) + "\n"
      if "#SBATCH -t " in line:
        outline = "#SBATCH -t " + time +  "\n"

    elif device == 'mic':
      ompLine = "setenv MIC_OMP_NUM_THREADS " + str(nThreadsPerRank) + "\n" + \
                "setenv MIC_PPN " + str(nRanksPerNode) + "\n"
      if "#SBATCH -n" in line :
        outline = '#SBATCH -n ' + str(nNodes) + "\n"
      if "setenv SLURM_NPROCS" in line :
        outline = 'setenv SLURM_NPROCS ' + str(nNodes) + "\n"
      if "#SBATCH -p normal" in line:
        outline = "#SBATCH -p normal-mic \n"
      if "#SBATCH -t " in line:
        outline = "#SBATCH -t " + time +  "\n"
      if "ibrun $EXEROOT/cesm.exe >&! cesm.log.$LID" in line:
        outline = "ibrun.symm -m $EXEROOT/cesm.exe >&! cesm.log.$LID \n" 

    if "setenv OMP_STACKSIZE" in line :
       outline = ompLine 

    outputFile.write(outline)

  outputFile.close()
  inputFile.close()
  commandLine1 = "cp " + inputFileName + " " + inputFileName + ".org"
  errorMessage = "failed to copy " + inputFileName + " to *.org"
  shellCommand(commandLine1,errorMessage)
  commandLine2 = "cp " + outputFileName + " " + inputFileName
  errorMessage = "failed to copy " + outputFileName + " into " + inputFileName
  shellCommand(commandLine2,errorMessage)
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
            nRanksPerNode = rankCount
            nThreadsPerRank = nthreads[indx] 
            totalNtasks = nNodes * nRanksPerNode
            #build case name
            if isTest:
              caseName = testName + '.'
            
            caseName = caseName + cesmVersion + '.' + resolution[0]
            caseName = caseName + '.' + str(nNodes) + 'nodes'
            caseName = caseName + '.' + device
            caseName = caseName + '.' + compset
            caseName = caseName + '.' + compiler
            caseName = caseName + '.' + str(nRanksPerNode) + 'mpi'
            caseName = caseName + '.' + str(nThreadsPerRank) + 'omp'
            cdCommand = 'cd ' + caseName + ' '
            createNewCase = './create_newcase -case ' + caseName + ' -res ' + resolution[0] \
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
            #xmlchangeLines.append('./xmlchange -file env_run.xml -id STOP_N -val 5')
            #xmlchangeLines.append('./xmlchange -file env_run.xml -id STOP_OPTION -val ndays')
            #xmlchangeLines.append('./xmlchange -file env_run.xml -id REST_OPTION -val never')
            #xmlchangeLines.append('./xmlchange -file env_run.xml -id TIMER_LEVEL -val 9')
            #xmlchangeLines.append('./xmlchange -file env_run.xml -id DOUT_S -val FALSE')
            #xmlchangeLines.append('./xmlchange -file env_run.xml -id COMP_RUN_BARRIERS -val FALSE')
            #xmlchangeLines.append('./xmlchange -file env_run.xml -id COMP_RUN_BARRIERS -val TRUE')
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
              commandLine = commandLine + ' &&' + xmlchangeMaxTaskPerNode + '32'
            if device == 'mic':
              commandLine = commandLine + ' &&' + xmlchangeMaxTaskPerNode + '244'
            commandLine = cdCommand + '&&' + commandLine 
            errorMessage = "failed at entering the new case directory or doing xmlchange of pes"
            shellCommand(commandLine,errorMessage)

            commandLine = cdCommand + ' && ./cesm_setup -clean && ./cesm_setup'
            errorMessage = "failed at entering  " + caseName + " directory or doing ./cesm_setup "
            shellCommand(commandLine,errorMessage)
            
            commandLine = cdCommand + ' && ' + caseName + '.clean_build'
            errorMessage = "failed at entering  " + caseName + " directory or doing clean_build "
            shellCommand(commandLine,errorMessage)

            if (device == 'mic') and (quad):
              commandLine = "cp quadrature_mod.F90 " + caseName + "/SourceMods/src.cam ."
              errorMessage = "failed at copying quadrature_mod.F90 into  " + caseName
              shellCommand(commandLine,errorMessage)
            
            if (device == 'mic'):
              simTime = '04:30:00'
            elif (device == 'host'):
              simTime = '01:30:00'
             
            fixCaseRunFile(caseName, device, nThreadsPerRank, nRanksPerNode, nNodes, simTime)

            commandLine = cdCommand + ' && ' + caseName + '.build'
            errorMessage = "failed at entering " + caseName + "directory or doing build "
            shellCommand(commandLine,errorMessage)
  
            commandLine = cdCommand + ' && ' + caseName + '.submit'
            errorMessage = "failed at entering " + caseName + "directory or doing submitting "
            shellCommand(commandLine,errorMessage)
         
            caseName = '' # clear the name

if __name__ == "__main__":
   main(sys.argv[1:])

