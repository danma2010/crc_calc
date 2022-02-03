#! python

########################################################
# S2H Programming
# Dan Mayaffit
#
# Feb 2020
# Calculate the equations for parallel CRC Calculation
########################################################


import re
#import time
import sys

def helpString():
    '''
    CRC Parallel Equetion CALCULATOR
    ----------------------------------
    Will print the actual equations for each bit to calculate the parallel CRC 
    for a given Poly
    
    gets:
        1. poly as a HEX number
        2. the word with as decimal number
        
    CRC Examples:
        CRC-32: 0x100050003
        CRC-4 : 0x19
    
    
    Returns
    -------
    None.
    
    Example
    -------
    for CRC-32 and 32-bit word width:
    >> python .\crc_calc.py 0x100050003 32
    
    

    '''

#print ('Hello, world!')
def crcCalculate(poly, wordWidth):
    #sampData = [1, 1, 0, 1, 1, 0, 0, 1]

    #dataW = 4
    #dataW = 32
    dataW = int(wordWidth)

    XOR = ' ^ '
    #crcPolyHexInput = int(0x19) # 11001 CRC-4
    #crcPolyHexInput = int(0x100050003) # CRC-32
    crcPolyHexInput = int(poly, base=16)

    #crcPolyShift = int(crcPolyHexInput)
    crcPolyShift = crcPolyHexInput

    polyList = []
    crcList  = []
    dataList = []
    equationList = []
    crcLen = 0

    for i in range(dataW):
        dataList.append('d'+str(i))
        i = i+1

    # make the list-array for the poly
    crcLen = 0
    while crcPolyShift > 0:
        polyList.append(crcPolyShift %2)
        crcPolyShift = int(crcPolyShift/2)
        crcList.append('c'+str(crcLen))
        equationList.append('c'+str(crcLen)+' = ')
        crcLen = crcLen+1
    
    # remove the '1' in the MSB of the polyList.
    # it's always '1' and will cause complication further.
    print(polyList)
    polyList[crcLen-1] = 0
    
    # start the equation calc
    #print(crcList)
    
    # make the shift process
    for i in range(dataW-1, -1, -1):
        for j in range(crcLen-1, 0, -1):
            if polyList[j]==1:
                crcList[j] = crcList[crcLen-1] + XOR + crcList[j-1]
            else:
                crcList[j] = crcList[j-1]
    
        # now move-in the next data
        if polyList[0] == 1:
            crcList[0] = crcList[crcLen-1] + XOR + dataList[i]
        else:
            crcList[0] = dataList[i]
    
    for i in range(crcLen):
        equationList[i] = equationList[i] + crcList[i]
    
    
    
    
    #print(polyList)
    #print(dataList)
    #print(crcList)
    #print(equationList)
    
    for i in equationList:
        print(i)
    
    



#--------------
if __name__ == "__main__":
    # start the main code when called from console
   print(" CRC Callculator \n")
    
   if len(sys.argv)== 1:
       print(helpString.__doc__)
   else:
       if len(sys.argv)== 2:
           poly = sys.argv[1]
           wordWidth = 32
           print ("=> got POLY: {}".format(poly))
           print ("No Word width entered, assuming {}".format(wordWidth))
       elif len(sys.argv)== 3:
           poly = sys.argv[1]
           wordWidth = sys.argv[2]
           print ("=> got POLY: {}\n".format(poly))
           print ("=> got wordWidth: {}\n\n".format(wordWidth))
           
       crcCalculate(poly, wordWidth)
    
       
       
      
    
        


    










 
      
    
        


    










