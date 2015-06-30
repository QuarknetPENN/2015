import time
from numpy import mean
from numpy import linspace
from scipy import stats
import matplotlib.pyplot as plt


def analysis(xin,yin,rin,plot):
    '''
    '''
    
    t0 = time.clock() #starts timer
    #Regression Test Arrays
    x = list(xin)
    y = list(yin)
    r = list(rin)
    xbar = mean(x)
    yadj = []
    xy = []
    xx = []
    n = len(x)
    computationTime = 0
    correlation = 0
    sst = []
    ssr = []
    
    b0, a0, r0 ,p0, s0 = stats.linregress(x,y)
    for i in range(0,n): #creates y_adj
        if (y[i] < (a0 + b0*x[i])):
            yadj.append(y[i] + r[i])
        else:
            yadj.append(y[i] - r[i])
    for i in range(0,n): #creates xy
        xy.append(x[i]*yadj[i])
    for i in range(0,n): #creates xx
        xx.append(x[i]**2)    
    sumxx = sum(xx)
    sumxy = sum(xy)
    yadjbar = mean(yadj)    
    a = ((yadjbar*sumxx - xbar*sumxy)) / (sumxx-n*(xbar**2)) #finds a
    b = (sumxy - n*xbar*yadjbar)/(sumxx-n*(xbar**2)) #finds b       
    
    for i in range(0,n): #creates ssxx
        sst.append((yadj[i]-yadjbar)**2)
    for i in range(0,n): #creates ssyy
        ssr.append(((a+b*x[i])-yadjbar)**2)    
    sst = sum(sst)
    ssr = sum(ssr)
    correlation = ssr/sst
    
    t1 = time.clock() #ends timer
    computationTime = t1 - t0 #calculates time
    
    if (plot == True):
        plt.scatter(x,y,1,'y')
        plt.scatter(x,yadj)
        plt.axis([min(x)-1,max(x)+1,min(yadj)-1,max(yadj)+1])
        axis = linspace(min(x),max(x))
        reg = a + b*axis
        plt.plot(axis,reg)
        plt.show()
    
    print ""
    print ""
    print ""
    print "-------------------------"
    print ""
    print "Linear Regression Results"
    print ""
    print "ComputationTime:   " + str(computationTime)
    print "a0:                " + str(a0)
    print "b0:                " + str(b0)
    print "a:                 " + str(a)
    print "b:                 " + str(b)
    print "Correlation:       " + str(correlation)
    print ""
    print "-------------------------"
    print ""
    print ""
    print ""

x = [2,4,8,12]
y = [2,4,4,4]
r = [0.6,0.8,0.3,0.2]

plot = False

analysis(x,y,r,plot)

#x = [12.0, 8.0, 4.0, 0.0]
#y = [4.0, 2.0, 4.0, 2.0]
#r = [1.2, 1, 0.8, 0.9]

#x = [1,5,9,13,17,21]
#y = [2,2,6,6,6,10]
#r = [0.2,1.4,1.5,0.2,0.9,1.9]

#x = [-2,2,4,8,12,16]
#y = [2,2,4,4,4,4]
#r = [0.1,0.6,0.8,0.3,0.2,0.9]