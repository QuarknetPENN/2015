# import relevant libraries
import time
start = time.clock()
import RPi.GPIO as GPIO
from math import sqrt, sin, cos, pi
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
print 'Importation takes', time.clock() - start, 'seconds'
start = time.clock()

#########################################
### I. SETUP & PRELIMINARY PROCESSING ###
#########################################
print '============= PART I ============='
 
# set up communication with the FPGA
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
in_pins = [10, 9, 11, 8, 7]     # 5 bits for incoming time data
out_pins = [17, 18, 27, 22, 24] # 5 bits for outgoing locations
for i in in_pins:
    GPIO.setup(i, GPIO.IN)
for i in out_pins:
    GPIO.setup(i, GPIO.OUT)
GPIO.setup(4, GPIO.IN)      # DATAREADY pin
GPIO.setup(14, GPIO.OUT)    # reset pin

def data_processing(location):
# ask the FPGA for time data from a given tube

    for i in range(len(location)):
        if location[i] == 1:
            GPIO.output(out_pins[i], True)
        else:
            GPIO.output(out_pins[i], False)
    loc_num = bits_to_decimal(location)

    if GPIO.input(4) == 1: # read DATAREADY to see if a tube fired
        
        # read timing pins
        FPGA_out = []
        for j in in_pins:
            FPGA_out.append(GPIO.input(j))
            
        # after reading pins, convert raw data to a radius
        radius = bits_to_decimal(FPGA_out) * .05
        print 'Tube', loc_num, 'fired with radius', radius
        return radius
    
    else: # assign radius = 0 to non-firing tubes
        return 0

def decimal_to_bits(decimal):
# converts numbers into arrays of 5 bits

    bits = []
    for i in [4, 3, 2, 1, 0]:
            if decimal - (2 ** i) >= 0:
                bits.append(1)
                decimal = (decimal - 2 ** i)
            else:
                bits.append(0)
    return bits

def bits_to_decimal(bits):
# converts an array of bits into a number

    decimal = 0
    for i in range(len(bits)):
        decimal += bits[i] * (2 ** (len(bits) - (i+1)))
    return decimal



x_loc = []
x_radii = []

while(1): # MAIN DATA PROCESSING LOOP: repeats indefinitely until 4 tubes fire
    
    # read data from each tube & write it into location & radius arrays
    for i in range(32):
        location = decimal_to_bits(i)   # create a binary location marker
        radius = data_processing(location)
        x_radii.append(radius)          # grow an array of ALL radii
        if radius > 0:                  # only add locations of tubes that fired
            x_loc.append(i)

    """
    # FAKE DATA :)
    x_radii = [0, 0, 0, 0, .35, 0, 0, 0, 0, 0, 0, 0, .75, 0, 0, 0, 0, 0, 0, 0, .8, 0, 0, 0, 0, 0, 0, 0, .2, 0, 0, 0]
    x_loc = [4, 12, 20, 28]
    """
    
    # clean up x_radii to include only nonzero radii
    while 0 in x_radii:
        x_radii.remove(0)

    # only datasets where 4 tubes fired get past this point
    if len(x_loc) != 4:
        print len(x_loc), 'tubes fired; resetting...'
        x_loc = []
        x_radii = []
        
        # fire a reset pulse; run the main loop again
        GPIO.output(14, True)
        GPIO.output(14, False)
        
    else:
        print 'WE GOT GOOD DATA!'
        break # 4-tube datasets go on to coordinate assignment

print 'X-tube locations: ' + str(x_loc)
print 'X-tube radii: ' + str(x_radii)
print 'Input processing takes', time.clock() - start, 'seconds'
start = time.clock()

#########################################
### II. A COORDINATE SYSTEM FOR TUBES ###
#########################################
print '============ PART II ============'

# the code below works only if chambers 1 & 2 face in the same direction

"""
# chamber heights are in cm, from lower scint (z=0) to top of chamber
h_ch1 = 46
h_ch2 = 20
# h_ch3 = 20
# h_ch4 = 15
R = 1.27 # tube radius = 1/2 inch = 1.27 cm

# assign coordinates to each tube that fired
def assign_coords(a_loc, height1, height2):
    a_tubes_b = [] # lateral (x/y) coordinates
    a_tubes_z = [] # vertical (z) coordinates

    # assign lateral coordinates
    for i in a_loc:
        row = i // 8            # each tube's row number (0-7)
        row_num = row % 2       # top/bottom row of a chamber (0/1)
        position = i - (row*8)  # lateral position within a row (0-7)
        b_coord = R * (2 - row_num + 2*position)
        a_tubes_b.append(b_coord)

        # assign vertical coordinates
        if row%4 <= 1:  # X-tube chambers
            a_tubes_z = z_coords(height1, row_num, a_tubes_z)
        else:           # Y-tube chambers
            a_tubes_z = z_coords(height2, row_num, a_tubes_z)
    return a_tubes_b, a_tubes_z

def z_coords(height, row_num, a_tubes_z):
    z_coord = height - R - (R * row_num * sqrt(3))
    a_tubes_z.append(z_coord)
    return a_tubes_z

x_tubes_y, x_tubes_z = assign_coords(x_loc, h_ch1, h_ch2)

 
print 'X-tube y-coords: ' + str(x_tubes_y)
print 'X-tube z-coords: ' + str(x_tubes_z)
# y_tubes_x, y_tubes_z = assign_coords(y_loc, h_ch3, h_ch4)
# print 'x-coords of Y-tubes: ' + str(y_tubes_x)
# print 'z-coords of Y-tubes: ' + str(y_tubes_z)
print 'Coordinate assignment takes', time.clock() - start, 'seconds'
start = time.clock()
"""

# some preliminary measurements
ch_ht = 5   # height of one chamber, in cm
sep = 26    # separation between tops of 2 chambers of the same orientation
init = 20   # height from bottom scintillator (z = 0) to top of chamber 4
R = 1.27    # tube radius (tube diameter = 1 inch = 2.54 cm)

# assign coordinates (x, y, z) to each tube that fired
# x and y are arbitrarily assigned; z is up
def assign_coords(a_loc, ch_ht, sep, init):
    a_tubes_b = [] # lateral (x/y) coordinates
    a_tubes_z = [] # vertical (z) coordinates

    for i in a_loc:
        # assign lateral coordinates
        row = i // 8                # each tube's row number (0-7)
        row_num = row % 2           # top/bottom row of a chamber (0/1)
        position = i - (row*8)      # lateral position within a row (0-7)
        b_coord = R * (2 - row_num + 2*position)
        a_tubes_b.append(b_coord)   # array of lateral coordinates

        # assign vertical coordinates
        alpha = i // 31             # 0 for X-tubes; 1 for Y-tubes
        beta = 1 - ((i // 16) % 2)  # 0 for ch. 1 & 3; 1 for ch. 2 & 4
        z_coord = init + (alpha * ch_ht) + (beta * sep) - R - (row_num * R*sqrt(3))
        a_tubes_z.append(z_coord)

    return a_tubes_b, a_tubes_z

x_tubes_y, x_tubes_z = assign_coords(x_loc, ch_ht, sep, init)
print 'X-tube y-coords: ' + str(x_tubes_y)
print 'X-tube z-coords: ' + str(x_tubes_z)
print 'Coordinate assignment takes', time.clock() - start, 'seconds'
start = time.clock()

#########################################
### III. MINIMIZATION AND MUON TRACKS ###
#########################################
print '============== PART III =============='

# minimize the value of an error function of 2 variables (mu, s)
# use brute force to find (mu, s) that minimize the function
def minimizer(a_tubes_b, a_tubes_z, a_radii, lat, vert, step1, step2):
    min_val = 10 ** 10 # an obscenely high 'guess'

    # iterate function evaluations over (mu, s)
    for mu in np.arange((-1*lat/vert), lat/vert, step1):
        for s in np.arange(0, lat, step2):
            
            SSE = error_funct(mu, s, a_tubes_b, a_tubes_z, a_radii)
            if SSE <= min_val: # reassign values for each new minimum
                min_val = SSE
                mu_a = mu
                a_s = s
                
    RMS = sqrt(min_val/len(a_tubes_b)) # compute root mean squared error
    return mu_a, a_s, RMS

# least-squares error function; outputs sum of squared errors (SSE)
def error_funct(mu, s, a_tubes_b, a_tubes_z, a_radii):
    SSE = 0 # sum each error term to find SSE
    for k in range(len(a_tubes_b)):
        numer = abs((a_tubes_z[k] * mu) + s - a_tubes_b[k])
        denom = sqrt(1 + (mu ** 2))
        error = (numer / denom) - a_radii[k]
        SSE += error ** 2
    return SSE

lat = 23.0  # side length of the (square) scintillator panel
vert = 75.0 # total height (distance between scintillators)
# increments of the variable search (mu)
step1 = .005
step2 = .1
evaluations = int(((2*lat/vert)/step1)*(lat/step2)) # number of function evaluations

print 'Minimizing the X-tube jawn with', evaluations, 'evaluations'
mu_y, y_s, RMS_x = minimizer(x_tubes_y, x_tubes_z, x_radii, lat, vert, step1, step2)
print 'mu_y =', mu_y
print 'y_s =', y_s
print 'X-tube error =', RMS_x
print 'X-tube minimization takes', time.clock() - start, 'seconds' 

# plot tubes that fired, their hit radii, and the best-fit line
def super_plotter(mu, s, a_tubes_b, a_tubes_z, R, a_radii):
    for i in range(len(a_tubes_b)):
        # set up some arrays
        b_param = []
        z_param = []
        b_drift = []
        z_drift = []
        
        # plot active tubes' center points
        plt.scatter(a_tubes_b[i], a_tubes_z[i], c = 'b')

        # plot tubes' outlines & drift circles parametrically
        for j in np.arange(0, 2*pi, .01): # numbers 0 to 2pi are parametrized:
            b_param.append(R * cos(j) + a_tubes_b[i]) # x = r*cos(i) + x0
            z_param.append(R * sin(j) + a_tubes_z[i]) # y = r*cos(i) + y0
    
            b_drift.append(a_radii[i] * cos(j) + a_tubes_b[i])
            z_drift.append(a_radii[i] * sin(j) + a_tubes_z[i])
            
        plt.plot(b_param, z_param, c = 'b')     # tube otlines
        plt.plot(b_drift, z_drift, c = 'black') # drift circles

    # plot best fit line
    b_val = [0, 20]
    z_val = [(1/mu)*(0-s), (1/mu)*(20-s)]
    plt.plot(b_val, z_val, c = 'r')
    plt.axis([0, 50, 0, 50])

# call functions
graph_x_tubes = super_plotter(mu_y, y_s, x_tubes_y, x_tubes_z, R, x_radii)
plt.show()
