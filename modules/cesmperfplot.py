# rects =  plt.bar(pos, cam3RatioArray, width, color='g')

def autolabelRel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        if (height == 0):
          print "skiping top label b/c zero"
        else:
          plt.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%.2f'%float(height),
                ha='center', va='bottom')

