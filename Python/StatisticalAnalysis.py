import time
from numpy import mean
from numpy import linspace
import matplotlib.pyplot as plt

#test arrays
x = [12.0, 8.0, 4.0, 0.0]
y = [4.0, 2.0, 4.0, 2.0]
r = [1.2, 1, 0.8, 0.9]
xbar = mean(x)

d = []
xd = []
xx = []
n = len(x)
computationTime = 0
t0 = time.clock()

for i in range(0,n):
    d.append(y[i] - r[i])
for i in range(0,n):
    xd.append(x[i]*d[i])
for i in range(0,n):
    xx.append(x[i]**2)
    
    
    
a = ((mean(d)*(sum(xx)) - mean(x)*sum(xd))) / (sum(xx)-n*(mean(x)**2))
b = (sum(xd) - n*mean(x)*mean(d))/(sum(xx)-n*(mean(x)**2))

t1 = time.clock()

computationTime = t1 - t0

print 'x: ' + str(x)
print 'y: ' + str(y)
print 'r: ' + str(r)
print 'd: ' + str(d)
print 'xx: ' + str(xx)
print 'xd: ' + str(xd)
print 'n: ' + str(n)
    
print "a: " + str(a)
print "b: " + str(b)
print "Capital R Squared: " + str(computationTime)

plt.scatter(x,y)
axis = linspace(min(x),max(x),100)
reg = a + b*axis
plt.plot(axis,reg)
plt.show()