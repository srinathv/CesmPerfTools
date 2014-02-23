#! /usr/bin/env python 
# simple python code to always git add pertanant CESM info from scripts directories.

#files we want to add:
#input: case directory name
import os,sys,getopt


def main(argv):
  dirName = ''
  howToUse = 'provGitAdd.py -d <case dir name at scripts level>'
  gitCom = 'git add '
  try:
    opts, args = getopt.getopt(argv,"hd:",["dirname="])
  except getopt.GetoptError:
        print howToUse
        sys.exit(2)
  for opt, arg in opts:
      if opt == '-h':
         print howToUse
         sys.exit()
      elif opt in ("-d", "--dirname"):
         dirName = arg
  files2Add=['Depends.*','Macros','README.*',dirName +'.out',dirName + '.run','env_*']
  dirs2Add=['SourceMods','logs','timing']

#now we have dir name iterate git adds over files
  for i in files2Add:
      os.system(gitCom + dirName + '/' + i)
      print gitCom + dirName + '/' + i
  for i in dirs2Add:
      print gitCom + dirName + '/' + i + '/*'
      os.system(gitCom + dirName + '/' + i + '/*')
       
if __name__ == "__main__":
   main(sys.argv[1:])

