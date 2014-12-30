#! /usr/bin/env python
#  parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                   help='an integer for the accumulator')
#this above syntax is for positional arguments
  #parser.add_argument('-r','--rundir', , action='store_const', ### dest defaults to --<name> if --<name> is used


import sys,os,getopt,argparse,math
import numpy as np
import matplotlib.pyplot as py
sys.path.append('../modules')
try:
  import cesmperftiming as cpt
except:
  print "Error: could not files cesmTimer module"
  sys.exit(1)


def calcAvg(theDir,groupTime): #which thing to average and get std
  primRunList=[]
  numList=[]
  flist=os.listdir(".")
  for fileName in flist:
    if ("HommeTime." in fileName):
      suffix=fileName.split(".")[1]
      if (suffix.isdigit()):
        numList.append(int(suffix))
  for i in numList:
    print i 
    parser=cpt.cesmTimeParser()
    try:
      parser.parseFile("HommeTime." + str(i))
    except:
      print "Error: There seems to be no HommeTime.<number> files."
      sys.exit(1)
    try:
      primRunList.append(parser.getDataEntry(groupTime,"wallmax"))
    except:
      print "Error: The " + groupTime + " seems not to be in the HommeTime files."
      sys.exit(1)
  
  num= len(numList) 
  print "number of members = ", num
  array=np.array(primRunList)
  avg =  np.average(array)
  std = np.std(array)  
  print "avg = ", avg
  print "std = ", std 
  print "number of members = ", num

  return avg,std,array,num

def calcZScore(avg1,std1,num1,avg2,std2,num2):
  numerator=abs(avg1-avg2)
  denom=math.sqrt(((std1**2)/num1)+(std2**2)/num2)
  zScore=numerator/denom
  return zScore
  

def main():
  parser = argparse.ArgumentParser(description='Given a directory with multiple post-indexed HommeTime files, this will '\
                                                'calculate averages and standard deviations.  Also, a histogram will be generated')
  parser.add_argument('-r','--rundir', dest='rundir', default='.',
                      help='Name of directory.')

  parser.add_argument('-n','--numbins', default=50,type=int,
                      help='Number of bins for historgram.')

  parser.add_argument('-f','--figurename', default=None,
                      help='Name of histogram figure.')
  
  parser.add_argument('-t','--figuretitle', default="NE=3, 1 mpi rank at full device thread use" ,
                      help='Title on histogram figure.')

  parser.add_argument('-g','--grouptime', default="prim_run",
                      help='Group timing desired.')

  parser.add_argument('-z','--zToRundir', dest='zToRundir', default=None,
                      help='Name of second directory of which to calculate z score.')
 
  parser.add_argument('-p','--plot',action="store_true",
                      help='Will plot.  If -f is given then figurename is used for saved figure.')

  args = parser.parse_args()


  currentDir=os.getcwd()
  try:
    os.chdir(args.rundir)
  except:
    print "Error: there seems not to be a " + args.rundir
    sys.exit(1)

  thisDir=os.getcwd().split("/")[-1]
  runDirAvg,runDirStd,primRunArray,numRunDir=calcAvg(thisDir,args.grouptime)

  if (args.plot) or (args.figurename):
    fig1=py.figure(num=None, figsize=(8, 8), dpi=80, facecolor='w', edgecolor='k')
    ax = fig1.add_subplot(1,1,1,)
    n,bins,patches=ax.hist(primRunArray,bins=args.numbins)
    py.xlabel(args.grouptime + "[sec]")
    py.ylabel("Number of Homme trials")
    py.title(thisDir + "\n "+ args.figuretitle + "\n" +
             "Avg =" + str(runDirAvg) + ", Std = " + str(runDirStd) )
    
    if args.figurename:
      py.savefig(args.figurename)
    else:
      py.show()


  os.chdir(currentDir)
  if args.zToRundir:
    print "we have a ztoRundir"
    try:
      os.chdir(args.zToRundir)
      thisDir=os.getcwd().split("/")[-1]
    except:
      print "Error: there seems not to be a " + args.rundir
      sys.exit(1)

    twoDirAvg,twoDirStd,twoRunArray,twoNumDir=calcAvg(thisDir,args.grouptime)
    zScore=calcZScore(runDirAvg,runDirStd,numRunDir,twoDirAvg,twoDirStd,twoNumDir)
    print "zScore is " + str(zScore)

  else:
     print "no zRunDir"


if __name__ == "__main__":
   main()
