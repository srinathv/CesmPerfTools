#! /usr/bin/env python

import sys,os,getopt,argparse,math
import numpy as np
import matplotlib.pyplot as py
sys.path.append('../modules')
try:
  import cesmperftiming as cpt
  import cesmperfplotting as cpp
except:
  print "Error: could not files cesmTimer module"
  sys.exit(1)
import calcAvgHommeTiming as caht

def main():
  parser = argparse.ArgumentParser(description='Given a directory with multiple post-indexed HommeTime files, this will '\
                                                'calculate averages and standard deviations.  Also, a histogram will be generated')

  parser.add_argument('-f','--figurename', default=None,
                      help='Name of histogram figure.')
  
  parser.add_argument('-t','--figuretitle', default="NE=3, 1 mpi rank at full device thread use" ,
                      help='Title on histogram figure.')

  parser.add_argument('-g','--grouptime', default="prim_run",
                      help='Group timing desired.')
  
  parser.add_argument('-l','--listRundir', dest='listRundir', default=None,
                      help='list of Rundirs to use for a line plot. Comma seperated')
  args = parser.parse_args()

  currentDir=os.getcwd()

#make line plot of averages with std error bars
  if args.listRundir:
    listOfDirs=[x.strip() for x in args.listRundir.split(',')]
    eachList=[]
    bigList=[]
    for dirs in listOfDirs: #make list of values
      print dirs
      try:
        os.chdir(dirs)
        thisDir=os.getcwd().split("/")[-1]
      except:
        print "Error: there seems not to be a " + thisDir
        sys.exit(1)
      avg,std,array,num=caht.calcAvg(thisDir,args.grouptime)
      eachList=[dirs,avg,std]
      bigList.append(eachList)
      os.chdir(currentDir)
    print bigList
    #plot
#    pos = np.arange(int(np.size(names)))    # the bar centers on the x axis
#    width = 0.35
#    newpos=pos+width
#    plt.rc(('xtick','ytick','axes'), labelsize=20.0)
#
#    fig=plt.figure(figsize=(12,14))
#    ax1=fig.add_subplot(111)
#    #ax2=fig.add_subplot(212)
#
#    ratioBars=ax1.bar(newpos, ratios, width, color='b')
#    ax1.set_ylabel('different', fontsize=20)
#    ax1.set_xticks(newpos)
#    ax1.set_xticklabels( names, rotation=80,fontsize=20)
#    #
#    ax1.set_title('Stampede FC5, ne16_ne16 \n' +
#              '(compiler: intel/13.1.1.163 , impi: impi/4.1.1.036 ) \n' +
#              '2 nodes, for each node: \n'+
#              'Host: 2 omp threads for each of 16 MPI ranks \n' +
#              'KNC: 48 omp threads for each 4 MPI ranks \n ' +
#              'Percentage of DRIVER_RUN_LOOP' ,fontsize=20.)
#
#    for t in ax1.get_yticklabels():
#        t.set_color('b')
#    strPercents=['%.1f'%x + '%' for x in percents]
#        
#    cpp.autolabelRel(ratioBars,strPercents)
#    else:
#      print "missing the list to bar plot"
#      sys.exit(1)
#

if __name__ == "__main__":
   main()

