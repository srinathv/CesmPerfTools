# rects =  plt.bar(pos, cam3RatioArray, width, color='g')


import matplotlib.pyplot as plt

def autolabelRel(rects,texts=None,fs=16,theColors=None):
    # attach some text labels
    for i in range(len(rects)):
    #for rect in rects:
      height = rects[i].get_height()
      if texts == None:
        word =  '%.2f'%float(height)
      else:
        word = texts[i]
      if (theColors == None) or (theColors =='black'):
        myColor='black'
      else: 
        myColor = theColors[i]
      if (height == 0):
        print "skiping top label b/c zero"
      else:
        plt.text(rects[i].get_x()+rects[i].get_width()/2., 1.01*height, word,
              ha='center', va='bottom',fontsize=16,color=myColor)

