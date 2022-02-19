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

    resource:
    https://www.embeddedrelated.com/showarticle/669.php
    http://srecord.sourceforge.net/crc16-ccitt.html
    http://www.ross.net/crc/download/crc_v3.txt
    https://www.drdobbs.com/implementing-the-ccitt-cyclical-redundan/199904926

    Example:
    for CRC-32 and 32-bit word width:
    >> python .\crc_calc.py 0x100050003 32
    '''
    #Class Object Attribute
    r = 5
    CRC16 = int(0x11021) # CRC16
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
        self.testInput = ['0x1234', '0x5678', '0x9abc', '0xdefc']
        self.testCRC = 0
        self.crcLen = 0
        print('new CRC instance')

    def makeDataList(self):
        self.dataList = []
        # make the list to hold the data-poly
        for i in range(self.dataW):
            self.dataList.append('d' + str(i))
        print("dataList: {}".format(self.dataList))

    def makePolyList(self):
        self.crcLen = 0
        crcPolyShift = self.crcPolyHexInput
        polyList = []

        while crcPolyShift > 0:
            polyList.append(crcPolyShift % 2)
            crcPolyShift = int(crcPolyShift / 2)
            # make the CRC register
            self.crcLen = self.crcLen + 1

        self.polyList = polyList



    def crcCalcEquation(self):
        crcPolyShift = self.crcPolyHexInput

        self.makeDataList()

        # make the list-array for the poly
        self.makePolyList()

        for i in range(self.crcLen):
            self.crcList.append('c' + str(i))

        for i in range(self.crcLen):
            self.equationList.append('c'+str(i)+' = ')

        # remove the '1' in the MSB of the polyList.
        # it's always '1' and will cause complication further.
        #print(self.polyList)
        self.polyList[self.crcLen-1] = 0

        # start the equation calc
        print("crcList: {}".format(self.crcList))

        # make the shift process
        # shift over the data register (data iterations) and the CRC bits
        for i in range(self.dataW-1, -1, -1):
            for j in range(self.crcLen-1, 0, -1):
                # if '1' gets to the MSB, xor it with the CRC reg, else just shift
                if self.polyList[j]==1:
                    self.crcList[j] = self.crcList[self.crcLen-1] + self.XOR + self.crcList[j-1]
                else:
                    self.crcList[j] = self.crcList[j-1]

            # now move-in the next data
            if self.polyList[0] == 1:
                self.crcList[0] = self.crcList[self.crcLen-1] + self.XOR + self.dataList[i]
            else:
                self.crcList[0] = self.dataList[i]

        # make the Equation
        for i in range(self.crcLen):
            self.equationList[i] = self.equationList[i] + self.crcList[i]

        print("The following are the equations for each bit")
        for i in self.equationList:
            print(i)

        #print(polyList)
        #print(self.dataList)
        #print(crcList)
        #print(equationList)

    
    def makeGolden(self):
        testInputList = []
        for i in self.testInput:
            i = int(i,16)
            print(i)
            #print("i:{} {}".format(i, int(i,base=16)))
            #for j in range(len(i));
            #testInputList.append()
            while i > 0:
                testInputList.append(i % 2)
                i = int(i / 2)
        print(testInputList)




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
    CRC.makeGolden()

    #CRC4 = CRCParallel('0x1001', 8)
    #CRC4.crcCalcEquation()
    
       
       
      
    
        


    










 
      
    
        


    










