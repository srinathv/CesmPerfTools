#! /usr/bin/env python

import sys,os,getopt,argparse
import numpy as np
import matplotlib.pyplot as py
sys.path.append('../modules')
try:
  import cesmperftiming as cpt
except:
  print "could not files cesmTimer module"


def main():
#def main(argv):
  parser = argparse.ArgumentParser(description='Given a directory with multiple post-indexed HommeTime files, this will '\
                                                'calculate averages and standard deviations.  Also, a histogram will be generated')
#  parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                   help='an integer for the accumulator')
#this above syntax is for positional arguments
  #parser.add_argument('-r','--rundir', , action='store_const', ### dest defaults to --<name> if --<name> is used
  parser.add_argument('-r','--rundir', dest='rundir', default='.',
                      help='Name of directory.')

  parser.add_argument('-n','--numbins', default=50,type=int,
                      help='Number of bins for historgram.')

  parser.add_argument('-f','--figurename', default=None,
                      help='Name of histogram figure.')
  args = parser.parse_args()

  os.chdir(args.rundir)

  thisDir=os.getcwd().split("/")[-1]

  primRunList=[]
  numList=[]
  flist=os.listdir(".")
  for fileName in flist:
    if ("HommeTime" in fileName):
      suffix=fileName.split(".")[1]
      if (suffix.isdigit()):
        numList.append(int(suffix))
  for i in numList:
    print i 
    parser=cpt.cesmTimeParser()
    parser.parseFile("HommeTime." + str(i))
    primRunList.append(parser.getDataEntry("prim_run","wallmax"))
    
  print "number of members = ", len(numList)
  primRunArray=np.array(primRunList)
  avg=  np.average(primRunArray)
  std = np.std(primRunArray)
  print "avg = ", avg
  print "std = ", std 


  fig1=py.figure(num=None, figsize=(8, 8), dpi=80, facecolor='w', edgecolor='k')
  ax = fig1.add_subplot(1,1,1,)
  n,bins,patches=ax.hist(primRunArray,bins=args.numbins)
  py.xlabel("prim_run [sec]")
  py.ylabel("Number of Homme trials")
  py.title(thisDir + "\n NE=3, 1 mpi rank at full device thread use \n" +
           "Avg =" + str(avg) + ", Std = " + str(std) )
  
  if args.figurename:
    py.savefig(args.figurename)
  else:
    py.show()


if __name__ == "__main__":
   main()
