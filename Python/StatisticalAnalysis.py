import time
from numpy import mean
from numpy import linspace
import matplotlib.pyplot as plt

#test arrays
x = [12.0, 8.0, 4.0, 0.0]
y = [4.0, 2.0, 4.0, 2.0]
r = [1.2, 1, 0.8, 0.9]
ybar = mean(y)

y_adj = []
xy = []
xx = []
n = len(x)
computationTime = 0

t0 = time.clock()

for i in range(0,n):
    if (y[i] < ybar):
        y_adj.append(y[i] + r[i])
    else:
        y_adj.append(y[i] - r[i])
for i in range(0,n):
    xy.append(x[i]*y_adj[i])
for i in range(0,n):
    xx.append(x[i]**2)
    
    
    
a = ((mean(y)*(sum(xx)) - mean(x)*sum(xy))) / (sum(xx)-n*(mean(x)**2))
b = (sum(xy) - n*mean(x)*mean(y))/(sum(xx)-n*(mean(x)**2))

t1 = time.clock()

computationTime = t1 - t0

print 'x: ' + str(x)
print 'y: ' + str(y)
print 'r: ' + str(r)
print 'y_adj: ' + str(y_adj)
print 'xx: ' + str(xx)
print 'xy: ' + str(xy)
print 'n: ' + str(n)
    
print "a: " + str(a)
print "b: " + str(b)
print "Capital R Squared: " + str(computationTime)

plt.scatter(x,y)
axis = linspace(min(x),max(x),100)
reg = a + b*axis
plt.plot(axis,reg)
plt.show()