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


class CRCParallel:
    '''
    CRC Parallel Equation CALCULATOR
    ----------------------------------
    Will print the actual equations for each bit to calculate the parallel CRC 
    for a given Poly
    gets:
        1. poly as a HEX number
        2. the word with as decimal number
        
    CRC Examples:
        CRC-32: 0x100050003
        CRC-4 : 0x19

    Returns: None.
    
    Example:
    for CRC-32 and 32-bit word width:
    >> python .\crc_calc.py 0x100050003 32
    '''
    #Class Object Attribute
    r = 5
    CCITT_CRC16 = int(0x11021) # CRC16
    CRC4  = int(0x19) # 11001 CRC-4
    CRC32 = int(0x100050003) # CRC-32


    def __init__(self, poly, wordWidth):
        self.poly = poly
        # make the poly to a HEX number
        self.crcPolyHexInput = int(poly, base=16)
        #self.crcPolyHexInput = poly
        #self.wordWidth = wordWidth
        self.dataW = int(wordWidth)
        self.polyList = []
        self.crcList  = []
        self.dataList = []
        self.equationList = []
        self.XOR = ' ^ '
        #self.crcMatrix = [][]
        print('new CRC instance')

    def makeDataList(self):
        self.dataList = []
        # make the list to hold the data-poly
        for i in range(self.dataW):
            self.dataList.append('d' + str(i))

    def crcCalcEquation(self):
        crcPolyShift = self.crcPolyHexInput

        self.makeDataList()

        # make the list-array for the poly
        crcLen = 0
        while crcPolyShift > 0:
            self.polyList.append(crcPolyShift %2)
            crcPolyShift = int(crcPolyShift/2)
            # make the CRC register
            self.crcList.append('c'+str(crcLen))
            # make the Equation list
            self.equationList.append('c'+str(crcLen)+' = ')
            crcLen = crcLen+1

        # remove the '1' in the MSB of the polyList.
        # it's always '1' and will cause complication further.
        #print(self.polyList)
        self.polyList[crcLen-1] = 0

        # start the equation calc
        #print(crcList)

        # make the shift process
        # shift over the data register (data iterations) and the CRC bits
        for i in range(self.dataW-1, -1, -1):
            for j in range(crcLen-1, 0, -1):
                # if '1' gets to the MSB, xor it with the CRC reg, else just shift
                if self.polyList[j]==1:
                    self.crcList[j] = self.crcList[crcLen-1] + self.XOR + self.crcList[j-1]
                else:
                    self.crcList[j] = self.crcList[j-1]

            # now move-in the next data
            if self.polyList[0] == 1:
                self.crcList[0] = self.crcList[crcLen-1] + self.XOR + self.dataList[i]
            else:
                self.crcList[0] = self.dataList[i]

        # make the Equation
        for i in range(crcLen):
            self.equationList[i] = self.equationList[i] + self.crcList[i]
    
    
    
    
        #print(polyList)
        #print(self.dataList)
        #print(crcList)
        #print(equationList)

        print("The following are the equations for each bit")
        for i in self.equationList:
            print(i)
    
    



#--------------
if __name__ == "__main__":

    # start the main code when called from console
    print(" CRC Callculator \n")

    if len(sys.argv)== 1:
        #CRCCalc
        CRCnone = CRCParallel('0x1011',2)
        print(CRCnone.__doc__)
    else:
       if len(sys.argv)== 2:
           poly = sys.argv[1]
           wordWidth = 32
           print ("=> got POLY: {}".format(poly))
           print ("No Word width entered, assuming {}".format(wordWidth))
           #CRC = CRCParallel(poly, wordWidth)

       elif len(sys.argv)== 3:
           poly = sys.argv[1]
           wordWidth = sys.argv[2]
           print ("=> got POLY: {}\n".format(poly))
           print ("=> got wordWidth: {}\n\n".format(wordWidth))

    CRC = CRCParallel(poly, wordWidth)
    print(CRC.__doc__)
    CRC.crcCalcEquation()
    
       
       
      
    
        


    










 
      
    
        


    










