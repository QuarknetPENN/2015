import time
from numpy import mean
from numpy import linspace
import matplotlib.pyplot as plt

#Regression Test Arrays

x = [12.0, 8.0, 4.0, 0.0]
y = [4.0, 2.0, 4.0, 2.0]
r = [1.2, 1, 0.8, 0.9]
xbar = mean(x)
ybar = mean(y)

y_adj = []
xy = []
xx = []
n = len(x)
computationTime = 0
correlation = 0
ssxx = []
ssyy = []
ssxy = []



#Regression Computation

t0 = time.clock() #starts timer

for i in range(0,n): #creates y_adj
    if (y[i] < ybar):
        y_adj.append(y[i] + r[i])
    else:
        y_adj.append(y[i] - r[i])
for i in range(0,n): #creates xy
    xy.append(x[i]*y_adj[i])
for i in range(0,n): #creates xx
    xx.append(x[i]**2)
    
sumxx = sum(xx)
sumxy = sum(xy)
    
a = ((ybar*sumxx - xbar*sumxy)) / (sumxx-n*(xbar**2)) #finds a
b = (sumxy - n*xbar*ybar)/(sumxx-n*(xbar**2)) #finds b

t1 = time.clock() #ends timer

computationTime = t1 - t0 #calculates time




# Regression Analysis         

for i in range(0,n): #creates ssxx
    ssxx.append((x[i]-xbar)**2)
for i in range(0,n): #creates ssyy
    ssyy.append((y[i]-ybar)**2)
for i in range(0,n): #creates ssxy
    ssxy.append(((y[i]-ybar)**2)*((x[i]-xbar)**2)) 
    
ssxx = sum(ssxx)
ssyy = sum(ssyy)
ssxy = sum(ssxy)

correlation = (ssxy**2)/(ssxx*ssyy)



#Regression Display

print 'x: ' + str(x)
print 'y: ' + str(y)
print 'r: ' + str(r)
print 'y_adj: ' + str(y_adj)
print 'xbar: ' + str(xbar)
print 'ybar: ' + str(ybar)

print "a: " + str(a)
print "b: " + str(b)
print "Correlation: " + str(correlation)
print "ComputationTime: " + str(computationTime)

plt.scatter(x,y)
axis = linspace(min(x),max(x),100)
reg = a + b*axis
plt.plot(axis,reg)
plt.show()