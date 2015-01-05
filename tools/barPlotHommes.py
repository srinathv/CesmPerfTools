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
    
      eachList=[dirs,avg,std,num]
      bigList.append(eachList)
      os.chdir(currentDir)

    zList=["base"]
    colorList=['black']
    percents=[""]
    for elem in bigList[1:]:
      zscore=caht.calcZScore(elem[1],elem[2],elem[3],bigList[0][1],bigList[0][2],bigList[0][3])
      per=(bigList[0][1]-elem[1])/bigList[0][1]
      if zscore > 2.33:
        isDiff='green'
      else:
        isDiff='red'
      theRelDiff=str('%.2f' % per + ' rel. diff') 
      zList.append(theRelDiff)
      colorList.append(isDiff)
      #zList.append(str('%.2f' % float(zscore)) + ' z, ' + str('%.2f' % per)  + '% rel. diff.')
    
    
        
      
    #plot
    pos = np.arange(int(len(bigList)))    # the bar centers on the x axis
    width = 0.35
    newpos=pos+width
    py.rc(('xtick','ytick','axes'), labelsize=20.0)

    fig=py.figure(figsize=(3*int(len(bigList)),2*int(len(bigList))))
    ax1=fig.add_subplot(111)
#    #ax2=fig.add_subplot(212)
    ratioBars=ax1.bar(newpos, [x[1] for x in bigList], width, color='b')
    #ratioBars=ax1.bar(newpos, [x[1] for x in bigList], width, color='b',yerr=[x[2] for x in bigList])
    ax1.set_ylabel(args.grouptime + ' [sec]', fontsize=15)
    ax1.set_xticks(newpos)
    ax1.set_xticklabels( [x[0] for x in bigList] , rotation=15,fontsize=10)
    ax1.set_title(args.figuretitle,fontsize=20.)
#
    #for t in ax1.get_yticklabels():
    #    t.set_color('b')
    cpp.autolabelRel(ratioBars,zList,12,colorList)
    if args.figurename:
      py.savefig(args.figurename)
    else:
      py.show()
  
  else:
      print "missing the list to bar plot"
      sys.exit(1)


if __name__ == "__main__":
   main()

