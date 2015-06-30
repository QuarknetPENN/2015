import time
from numpy import mean
from numpy import linspace
from numpy import pi
import matplotlib.pyplot as plt


def analysis(xin,yin,rin):
    '''
    '''
    
    #Regression Test Arrays
    x = list(xin)
    y = list(yin)
    r = list(rin)
    xbar = mean(x)
    ybar = mean(y)
    
    yadj = []
    xy = []
    xx = []
    n = len(x)
    computationTime = 0
    #correlation = 0
    #ssxx = []
    #ssyy = []
    #ssxy = []
    
    
    
    #Regression Computation
    
    t0 = time.clock() #starts timer
    
    for i in range(0,n): #creates y_adj
        if (y[i] < ybar):
            y[i] = y[i] + r[i]
        else:
            y[i] = y[i] - r[i]
    for i in range(0,n): #creates xy
        xy.append(x[i]*y[i])
    for i in range(0,n): #creates xx
        xx.append(x[i]**2)
        
    sumxx = sum(xx)
    sumxy = sum(xy)
    ybar = mean(y)
        
    a = ((ybar*sumxx - xbar*sumxy)) / (sumxx-n*(xbar**2)) #finds a
    b = (sumxy - n*xbar*ybar)/(sumxx-n*(xbar**2)) #finds b
    
    t1 = time.clock() #ends timer
    
    computationTime = t1 - t0 #calculates time
    
    
    
    # Regression Analysis         
    
    #for i in range(0,n): #creates ssxx
    #    ssxx.append((x[i]-xbar)**2)
    #for i in range(0,n): #creates ssyy
    #    ssyy.append((yadj[i]-yadjbar)**2)
    #for i in range(0,n): #creates ssxy
    #    ssxy.append(((yadj[i]-yadjbar)**2)*((x[i]-xbar)**2)) 
    #    
    #ssxx = sum(ssxx)
    #ssyy = sum(ssyy)
    #ssxy = sum(ssxy)
    #
    #correlation = (ssxy**2)/(ssxx*ssyy)
    
    
    
    #Regression Display
    
    print 'x: ' + str(x)
    print 'y: ' + str(y)
    print 'r: ' + str(r)
    print 'xbar: ' + str(xbar)
    print 'ybar: ' + str(ybar)
    
    print "a: " + str(a)
    print "b: " + str(b)
    #print "Correlation: " + str(correlation)
    print "ComputationTime: " + str(computationTime)
    
    area = []
    
    for i in range(0,n):
        area.append(pi*((129*r[i])**2))
    
    plt.scatter(x,y,area, 'y')
    axis = linspace(min(x),max(x),100)
    reg = a + b*axis
    plt.plot(axis,reg)
    plt.show()
  



#x = [12.0, 8.0, 4.0, 0.0]
#y = [4.0, 2.0, 4.0, 2.0]
#r = [1.2, 1, 0.8, 0.9]

analysis([12.0, 8.0, 4.0, 0.0],[4.0, 2.0, 4.0, 2.0],[1.2, 1, 0.8, 0.9])