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
        #self.crcListInd  = []
        #self.dataList = []
        self.equationList = []
        #self.cn = []
        self.dn = []
        self.XOR = ' ^ '
        #self.crcMatrix = [][]
        #self.testInput = ['0x1234', '0x5678', '0x9abc', '0xdefc']
        #self.testCRC = 0
        self.crcLen = 0
        #print('new CRC instance')

    def makeDataList(self):
        # make the list to hold the data inputs
        for i in range(self.dataW):
            #self.dataList.append('d' + str(i))
            self.dn.append('d' + str(i))
            #self.dn.append(self.dataList[i])
        print("dn: {}".format(self.dn))

    def makePolyList(self):
        # set the list of the bits for the Poly
        # list location 0 is LSB of the poly
        self.crcLen = 0
        crcPolyShift = self.crcPolyHexInput
        polyList = []

        while crcPolyShift > 0:
            polyList.append(crcPolyShift % 2)
            crcPolyShift = int(crcPolyShift / 2)
            # make the CRC register
            self.crcLen = self.crcLen + 1

        self.polyList = polyList
        self.crcLen = self.crcLen -1

    def makeCrcList(self):
        for i in range(self.crcLen):
            self.crcList.append('c' + str(i))
            #self.crcListInd.append([self.crcList[i]])
            #self.cn.append(i)

        for i in range(self.crcLen):
            self.equationList.append('c'+str(i)+' = ')



    def crcCalcEquation(self):
        #crcPolyShift = self.crcPolyHexInput

        self.makeDataList()
        self.makePolyList()
        self.makeCrcList()

        # remove the '1' in the MSB of the polyList.
        # it's always '1' and will cause complication further.
        #print(self.polyList)
        self.polyList[self.crcLen-1] = 0

        # start the equation calc
        #print("crcList:    {}".format(self.crcList))
        #print("crcListInd: {}".format(self.crcListInd))
        #print("cn: {}".format(self.cn))
        #print("dn: {}".format(self.dn))
        #print("crcLen: {}".format(self.crcLen))

        # make the shift process
        # shift over the current CRC register for the dataW cycles
        # each step set the XOR bits according to the poly 
        for i in range(self.dataW-1):
            cHigh = self.crcList[self.crcLen-1]
            for j in range(self.crcLen-1, 0, -1):
                if self.polyList[j]==1:
                    self.crcList[j] = cHigh + self.XOR + self.crcList[j-1]
                else:
                    self.crcList[j] = self.crcList[j-1]

            # now move-in the next data
            if self.polyList[0] == 1:
                self.crcList[0] = cHigh + self.XOR + self.dn[i]
            else:
                self.crcList[0] = self.dn[i]

        crcLisrSplit = []
        for i in self.crcList:
            crcLisrSplit.append(i.split(self.XOR))
        print(crcLisrSplit)

        # remove dulplicate items (as b^a^a^c = b^c)
        for cn in crcLisrSplit:
            removeList = []
            print("cn a: {}".format(cn))
            cn.sort()
            print("cn b: {}".format(cn))
            print(len(cn))
            for i in range(1,len(cn)):
                if (cn[i-1] == cn[i]):
                    removeList.append(cn[i-1])
                    removeList.append(cn[i])
            for k in removeList:
                cn.remove(k)

            print("cn c: {}".format(cn))

        for i in range(len(self.equationList)):
            #tmp = ""
            for j in crcLisrSplit[i]:
                #tmp = j + XOR
                self.equationList[i] = self.equationList[i] + j + self.XOR

        for i in self.equationList:
            print(i)


    def crcCalcEquation0(self):
        crcPolyShift = self.crcPolyHexInput

        self.makeDataList()

        # make the list-array for the poly
        self.makePolyList()

        self.makeCrcList()

        # remove the '1' in the MSB of the polyList.
        # it's always '1' and will cause complication further.
        #print(self.polyList)
        self.polyList[self.crcLen-1] = 0

        # start the equation calc
        print("crcList:    {}".format(self.crcList))
        #print("crcListInd: {}".format(self.crcListInd))
        print("cn: {}".format(self.cn))
        print("dn: {}".format(self.dn))
        print("crcLen: {}".format(self.crcLen))

        #for i in range(self.crcLen):
        #    self.crcListInd[i]=[]

        # make the shift process
        # shift over the current CRC register for the dataW cycles
        # each step set the XOR bits according to the poly
        for i in range(self.dataW-1):
            cHigh = self.crcList[self.crcLen-1]
            for j in range(self.crcLen-1, 0, -1):
                if self.polyList[j]==1:
                    #print(self.crcListInd[j])
                    #self.crcList[j]    = self.crcList[self.crcLen-1] + self.XOR + self.crcList[j-1]
                    self.crcList[j]    = cHigh + self.XOR + self.crcList[j-1]
                    #self.crcListInd[j] = self.crcListInd[j - 1]
                    #self.crcListInd[j].append(cHigh)
                else:
                    #print(self.crcListInd[j])
                    self.crcList[j] = self.crcList[j-1]
                    #self.crcListInd[j] = self.crcListInd[j-1]

            # now move-in the next data
            if self.polyList[0] == 1:
                self.crcList[0] = cHigh + self.XOR + self.dn[i]
                #self.crcListInd[0] = self.crcListInd[self.crcLen-1]
                #self.crcListInd[0].append(self.dn[i])
            else:
                self.crcList[0] = self.dn[i]
                #self.crcListInd[0] = self.dn[i]

        # make the Equation
        for i in range(self.crcLen):
            self.equationList[i] = self.equationList[i] + self.crcList[i]

        crcLisrSplit = []
        for i in self.crcList:
            crcLisrSplit.append(i.split(self.XOR))
        print(crcLisrSplit)

        #for cn in crcLisrSplit:
        #    for i in cn:



        print("\n\nThe following are the equations for each bit\n")
        for i in self.equationList:
            print(i)
        print("===========================================\n\n")

        #for i in self.crcListInd:
        #    print(i)

        #print(polyList)
        #print(self.dn)
        #print(crcList)
        #print(equationList)

    
    def makeGolden(self):
        testInputList = [0xf1111111, 0xf2222222, 0xf3333333]
        testBits = []
        for i in testInputList:
            #i = int(i,16)
            print(i)
            #print("i:{} {}".format(i, int(i,base=16)))
            #for j in range(len(i));
            #testInputList.append()
            while i > 0:
                testBits.append(i % 2)
                i = int(i / 2)

        print(testBits)
        print(self.polyList)

        #print(f'{0xABC123EFFF:0>42b}')



    #def hex2bin(self, x):


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
    #CRC.makeGolden()

    #CRC4 = CRCParallel('0x1001', 8)
    #CRC4.crcCalcEquation()
    
       
       
      
    
        


    










 
      
    
        


    











