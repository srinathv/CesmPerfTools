#! /usr/bin/env python

import os,sys,getopt
import subprocess
# this will run dg_kernel on listed machines and test different KMP_AFFINITY settings. 




#unset IBM variables on yellowstone:

unsetters="unsetenv MP_PE_AFFINITY; unsetenv MP_TASK_AFFINITY; unsetenv MP_CPU_BIND_LIST"
#on yellowstone, we should run with and without the unsetters.
# lists

granularity=['core','fine']
binding=['scatter','compact']
nthreads=[16,32]
compilers = {'eos':{'intel':['13.1.3.192'],'pgi':['13.7-0'],'cray':['8.1.9']},
             'stampede':{'intel':['13.1.1.163','14.0.1.106']},
             'yellowstone':{'intel':['13.1.2','14.0.1'],'pgi':['13.3','13.9']},
             'darwin':{'gfortran':['4.8.2'],'intel':['14.0.1']}}

compilerCommand = {'intel':'mpif90','pgi':'mpipf90','cray','ftn'}
# I guess we are assuming necessary parallel compilers


#at some point need to make a machines class that inherets from a compiler class and move module detection and loading 
#to the machine class.  A machine object will know all of the details of the machine such as compilers, run scripts,
#queing system, arhcitecture, job launcher and software handlers.

#on EOS:
#module swap PrgEnv-intel PrgEnv-cray



class buildAndRunObj(self):
  def __init__(self, source = ''):
    self.compiler = 'intel'
    self.compilerVersion = ''
    self.machine = ''
    self.compileFlags = ''
    self.source = source
    self.executable = ''
    self.envVars = '' # used for KMP setting and the like 'export KMP_AFFINITY=<>; export OMP_NUM_TRHEADS=<>; ./<exec>
                      #<output file name>' 
                      #
    self.args = '' # any arguments to the executable 

  def setCompiler(self,compiler):
    assert type(compiler) is StringType, "name is not a string: %r" % compiler
    self.compiler = compiler
  
  def setCompilerVersion(self,version):
    assert type(version) is StringType, "name is not a string: %r" % version
    self.compilerVersion = version

  def setMachine(sefl,machine):
    assert type(machine) is StringType, "name is not a string: %r" % machine
    self.machine = machine

  def setCompilerFlags(self,flags):
    assert type(flags) is StringType, "name is not a string: %r" % flags
    self.compileFlags = flags
  
  def setExecutable(self,exe):
    assert type(exe) is StringType, "name is not a string: %r" % exe
    self.executable = exe

 def setEnvVars(self,envars):
    assert type(envars) is StringType, "name is not a string: %r" % envvars
    self.envVars = envvars

 def setArgs(self,args):
    assert type(args) is StringType, "name is not a string: %r" % args
    self.setArgs = args


  def getCompiler(self):
    assert(self.compiler, "compiler not set")
    return self.compiler 
  
  def getCompilerVersion(self):
    assert(self.compilerVersion, "compilerVersion not set")
    return self.compilerVersion 

  def getMachine(sefl):
    assert(self.machine, "machine not set")
    return self.machine 

  def getCompilerFlags(self):
    assert(self.compileFlags, "comipleFlags not set")
    return self.compileFlags 

  def getExecutable(self):
    assert(self.executable, "executable not set")
    return self.executable

  def getEnvVars(self):
      assert(self.envVars, "envVars not set") 
      return self.envVars

  def getArgs(self):
      return self.args

#  def build(self,exName,machine,compiler,compVer,compFlags=''):
  def build(self,prefix='',suffix=''):
    machine = self.getMachine()
    compiler = self.getCompiler()
    version = self.getCompilerVersion()
    source = self.getSource()
    flags = self.getCompilerFlags() #this is where -D<> for ifdefs is specified
    
    mloadline = lcfCompModLoad(machine,compiler,version) #  module load string
    exName = prefix + '.' + machine + '.' + compiler + '.' + version + suffix
    self.setExecutable(exName)
#build command to compile: given machine and compiler use:
    command = compilerCommand[compiler] + ' ' + source + flags + ' -o ' + exName
    
    #    subprocess.call(buildLine,stdout=subprocess.STDOUT,stderr=subprocess.STDOUT,shell=True)
    command_process = subprocess.Popen(
      [command],
      shell=True,
     # stdin=subprocess.PIPE,
     # stdout=subprocess.PIPE,
      stdout=subprocess.STDOUT,
      stderr=subprocess.STDOUT,
    )
    command_output = command_process.communicate()[0]

    log_file = open(exName + '_build.log', 'a')
    log_file.write('[ % ]' % datetime.datetime.now())
    log_file.write('\n')
    log_file.write(command_output)
    log_file.write('\n')
    log_file.close() 
    #given machine, compiler and version do 
        #the correct module purge then loads
        #get compiler command
        #build compile line
        #subprocess command line

#for now, the run will be done without submission scripts
  def run(self,envVars = ''):
    



def lcfCompModLoad(machine,compiler,version):
    #given a machine, detect if compiler module is loaded
    #if loaded return string 'loaded'
    #if not then create new load string
    moduleLoaded = False #assume the module is not loaded
    moduleName = compiler + '/' + version
    moduleList=subprocess.check_output('module list',stderr=subprocess.STDOUT,shell=True).split() # makes list of output
    if moduleName in moduleList:
      moduleLoaded = True
      return mloadline = 'loaded'
    else
      #find module and create the correct line for module swap
      if machine == 'stampede':
        loadedCompiler=[x for x in moduleList if 'intel' in x]
      elif machine == 'yellowstone':
        loadedCompiler=[x for x in moduleList if 'intel' in x or 'pgi' in x]
      elif machine == 'eos':
        loadedCompiler=[x for x in moduleList if 'intel' in x or 'pgi' in x or 'cray' in x] ##THIS IS PROBABLY WRONG##
      elif machine == 'darwin':
        print ' on a mac, good luck'
      else:
        print 'machine not supported'
        sys.exit()
      return mloadline = 'module swap ' + loadedCompiler[0] + ' ' + moduleName
#should make a class of machines and attribues
      
       





def main(argv):
    machine = ''
    exectuable = ''
    howToUse = "testKmp.py -e <exetuable name if exsits, if not script will build defaults for machine> -m <machine if
given and if not, script will try to detect>"
    try:
      opts, args = getopt.getopt(argv,"he:m:",["exectuable=","machine="])
    except getopt.GetoptError:
       defaultBuild = true
       detectMachine = true
    for opt, arg in opts:
      if opt == '-h':
        print howToUse
        sys.exit()
      elif opt in ("-e","--executable"):
        exetuable = arg
      elif opt in ("-m", "--machine"):
        machine = arg

#We can add detection of machine later, but for now just specify"

#If executable is not passed, then build all for this machine.  Machine is always passed.
#FLOW:  given machine:
#   1)build executables for all compilers and versions
    for k in compilers[machine]: #vendor
        print k
        for j in compilers[i][k]: #version
            print j
            baseName=i+k+j
            exName='dg_kernel'+ baseName
            dgKRunObj=runObj(exName)
            dgKRunObj.setMachine=machine
            
            
                        
#   2)do run for each executable for all combinations of KMP affinit and MP settings on stampede


#detection of hostname:
#on stampede (in idev):
#c557-401$ hostname
#c557-401.stampede.tacc.utexas.edu

#yellostone (geyser Idev):
#$ hostname
#geyser01
#bash-4.1$ hostname -a
#gy0001.yellowstone geyser01

#eos (interactive)
#~> hostname
#eos-login2


if __name__ == "__main__":
   main(sys.argv[1:])
