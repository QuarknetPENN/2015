import time
from numpy import mean
from numpy import linspace
import matplotlib.pyplot as plt


def analysis(xin,yin,rin,plot):
    '''
    '''
    t0 = time.clock() #ends timer 
    #Regression Test Arrays
    x = list(xin)
    y = list(yin)
    r = list(rin)
    list1 = []
    list2 = []
    n = len(x)
    
    
    for i in range(0,n): #creates xx
        list1.append(x[i]**2)
    for i in range(0,n): #creates xy
        list2.append(x[i]*y[i])
    sum1 = sum(list1)  
    sum2 = sum(list2)
    avg1 = mean(x)
    avg2 = mean(y)
    a0 = ((avg2*sum1 - avg1*sum2)) / (sum1-n*(avg1**2)) #finds a
    b0 = (sum2 - n*avg1*avg2)/(sum1-n*(avg1**2)) #finds b  
    for i in range(0,n): #creates y_adj
        if (y[i] < (a0 + b0*x[i])):
            y[i] = y[i] + r[i]
        else:
            y[i] = y[i] - r[i]
    for i in range(0,n): #creates xy
        list2[i] = x[i]*y[i]   
    sum2 = sum(list2)
    avg2 = mean(y)    
    a = ((avg2*sum1 - avg1*sum2)) / (sum1-n*(avg1**2)) #finds a
    b = (sum2 - n*avg1*avg2)/(sum1-n*(avg1**2)) #finds b
    t1 = time.clock() #ends timer   
    
    for i in range(0,n): #creates ssxx
        list1[i] = (y[i]-avg2)**2
    for i in range(0,n): #creates ssyy
        list2[i] = ((a+b*x[i])-avg2)**2    
    sum1 = sum(list1)
    sum2 = sum(list2)
    correlation = sum2/sum1
    
    computationTime = t1 - t0 #calculates time
    
    if (plot == True):
        plt.scatter(x,y)
        plt.axis([min(x)-1,max(x)+1,min(y)-1,max(y)+1])
        axis = linspace(min(x),max(x))
        reg = a + b*axis
        plt.plot(axis,reg)
        plt.show()
    
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
    
#x = [12.0, 8.0, 4.0, 0.0]
#y = [4.0, 2.0, 4.0, 2.0]
#r = [1.2, 1, 0.8, 0.9]

#x = [1,5,9,13,17,21]
#y = [2,2,6,6,6,10]
#r = [0.2,1.4,1.5,0.2,0.9,1.9]

#x = [-2,2,4,8,12,16]
#y = [2,2,4,4,4,4]
#r = [0.1,0.6,0.8,0.3,0.2,0.9]

x = [2,4,8,12]
y = [2,4,4,4]
r = [0.6,0.8,0.3,0.2]

plot = True

#plot = False

analysis(x,y,r,plot)