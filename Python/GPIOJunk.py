import RPi.GPIO as GPIO

def setup():
    '''
    '''
    # set up communication with the FPGA
    GPIO.setwarnings(False) #does this cause any problems?
    GPIO.setmode(GPIO.BCM)
    in_pins = [10, 9, 11, 8, 7]     # 5 bits for incoming time data
    out_pins = [17, 18, 27, 22, 24] # 5 bits for outgoing locations
    for i in in_pins:
        GPIO.setup(i, GPIO.IN)
    for i in out_pins:
        GPIO.setup(i, GPIO.OUT)
    GPIO.setup(4, GPIO.IN)      # DATAREADY pin
    GPIO.setup(14, GPIO.OUT)    # reset pin
    
def binaryToDecimal(binary):
    '''
    '''
    decimal = 0
    for i in range(len(binary)):
        decimal += binary[i] * (2 ** (len(binary) - (i+1)))
    return decimal
    
def getTubeInfo(addresses, in_pins, out_pins):
    '''
    '''
    fullTube = True
    x = []
    y = []
    tubeRadii = []
    addresses = [ 
                [0,0,0,0,0] , [0,0,0,0,1] , [0,0,0,1,0] , [0,0,0,1,1] , [0,0,1,0,0] , [0,0,1,0,1] , [0,0,1,1,0] , [0,0,1,1,1] ,
                [0,1,0,0,0] , [0,1,0,0,1] , [0,1,0,1,0] , [0,1,0,1,1] , [0,1,1,0,0] , [0,1,1,0,1] , [0,1,1,1,0] , [0,1,1,1,1] ,
                [1,0,0,0,0] , [1,0,0,0,1] , [1,0,0,1,0] , [1,0,0,1,1] , [1,0,1,0,0] , [1,0,1,0,1] , [1,0,1,1,0] , [1,0,1,1,1] , 
                [1,1,0,0,0] , [1,1,0,0,1] , [1,1,0,1,0] , [1,1,0,1,1] , [1,1,1,0,0] , [1,1,1,0,1] , [1,1,1,1,0] , [1,1,1,1,1]
                ]
    # some preliminary measurements
    ch_ht = 5   # height of one chamber, in cm
    sep = 26    # separation between tops of 2 chambers of the same orientation
    init = 20   # height from bottom scintillator (z = 0) to top of chamber 4
    R = 1.27    # tube radius (tube diameter = 1 inch = 2.54 cm)
    for i in range(0,len(addresses)):
        address = addresses[i]
        tubeNumber = binaryToDecimal(address)
        for j in range(0,5):
            if address[j] == 1:
                GPIO.output(out_pins[j], True)
            else:
                GPIO.output(out_pins[j], False)
    
        for j in range(0,len(in_pins)):
            if in_pins[i] == 1 :
                fullTube = False
                break
            else:
                fullTube = True
    
        if fullTube:
            FPGA_out = []
            for j in in_pins:
                FPGA_out.append(GPIO.input(j))
                
            # after reading pins, convert raw data to a radius
            tubeRadii.append(binaryToDecimal(FPGA_out) * .05)
            # assign lateral coordinates
            row = tubeNumber // 8
            row_num = row%2
            position = i - (row*8)
            y.append(R*(2 - row_num + 2*position))
            # assign vertical coordinates
            alpha = i // 31             # 0 for X-tubes; 1 for Y-tubes
            beta = 1 - ((i // 16) % 2)  # 0 for ch. 1 & 3; 1 for ch. 2 & 4
            x.append(init + (alpha * ch_ht) + (beta * sep) - R - (row_num * R*sqrt(3)))