#! /usr/bin/env python

#####
# 

import subprocess
import os,sys,getopt

def shellCommand(command,errorMessage):
#command initiated where this script is ran
  try:
    print command
    subprocess.check_call(command, stderr=subprocess.STDOUT, shell=True)
  except :
    print errorMessage
    pass


def main():
  howToUse = 'scpDirs -l <wildcard list> -d <destination machine> -p <path to dump list and its contents>'
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hl:d:p:")
  except getopt.GetoptError:
        print howToUse
        sys.exit(2)
        #pass
  for opt, arg in opts:
      if opt in ('-h','--help'):
        print howToUse
        sys.exit()
      elif opt in ('-l', '--list'):
        wildCardList = arg
      elif opt in ('-d', '--destination'):
        machine = arg
      elif opt in ('-p', '--path'):
        destPath = arg
      else:
        assert False, "unhandled option" 

  #make list of from wild card
  cmd = 'echo ' + wildCardList
  cpList = shellCommand( cmd, 'wildcard list is not understood')
  print cpList 

        
         




if __name__ == "__main__":
   main()
