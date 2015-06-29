#SENDING TO FPGA
#Tube Address: 5 bit
#Reset:        1 bit

#RECEIVING FROM FPGA
#Tube Time: 5 bit

#OUTPUT OF PROGRAM
#Tube Data Array
tubeData = []

def toFiveBitBinary(decimalNumber):
    binaryString = ''
    for i in range(0,5):
        if 