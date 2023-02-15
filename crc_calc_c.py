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
#import numpy


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
    !!!!
    https://srecord.sourceforge.net/crc16-ccitt.html#overview
    !!!!

    Example:
    for CRC-32 and 32-bit word width:
    >> python .\crc_calc.py 0x100050003 32
    0x11021 16

    '''
    #Class Object Attribute
    #r = 5
    CRC16 = int(0x11021) # CRC16
    CRC4  = int(0x19) # 11001 CRC-4
    CRC32 = int(0x100050003) # CRC-32



    def __init__(self, poly, initValue, wordWidth):
        self.poly = poly
        self.initValue = initValue

        # make the poly to a HEX number
        self.crcPolyHexInput = int(poly, base=16)
        self.dataW = int(wordWidth)
        self.polyList = []
        #self.polyListInv = []
        self.crcList  = []
        self.testListNum = 0
        self.equationList = []
        self.equMatrix = []
        self.XOR = ' ^ '
        self.crcLen = 0
        # make the list which holds the poly
        self.makePolyList()

    def makePolyList(self):
        # set the list of the bits for the Poly
        # list location 0 is LSB of the poly
        #self.crcLen = 0
        crcPolyShift = self.crcPolyHexInput
        polyList = []

        while crcPolyShift > 0:
            polyList.append(crcPolyShift % 2)
            crcPolyShift = int(crcPolyShift / 2)
            # make the CRC register
            #self.crcLen = self.crcLen + 1

        # invert the list so that the MSB will be at location 0. the shift will be from the LSB
        self.polyList = polyList[::-1]
        #polyListInv = polyList[::-1]
        #self.polyListInv = polyListInv
        self.crcLen = polyList.__len__()-1
        #self.polyListInv = self.polyListInv + [0]*(self.dataW)
        print("======================================")
        print("poly: {}; order: {}; Data-Width: {}; polyList: \n{}".format(self.poly, self.crcLen, self.dataW, self.polyList))
        print("======================================")

    # the functions that calculates the CRC parallel equations
    def calcCRCEqu(self):
        crcLen = self.crcLen
        #dataWidth = self.dataW
        dataList = self.makeShiftRegList(self.dataW)
        crcEqList = []

        dataShift = dataList[:]

        # Calculate the parallel equations
        for shiftTime in range(dataList.__len__()-crcLen-1):
            #first Rshift then XOR
            for i in range(dataShift.__len__()-1):
                dataShift[i] = dataShift[i+1]
            dataShift[-1] = ['x']

            for j in range(crcLen,-1,-1):
                cHigh = dataShift[0]
                if self.polyList[j]==1:
                    dataShift[j] = dataShift[j] + cHigh

        # clean duplicates
        k = -1
        for i in dataShift:
            k = k+1
            cleanFlag = 1
            while cleanFlag:
                cleanFlag =0
                for j in i:
                    #print(i.count(j))
                    if (i.count(j)>1):
                        cleanFlag = cleanFlag + i.count(j)
                        #print("Clean list for: ({}): {}, {} x {}".format(k, i, i.count(j), j))
                        i.remove(j)
                        i.remove(j)

        #print the equations
        print("===== Parallel Equations =======")
        itemNum = crcLen
        for k in range(crcLen+1):  # enumerate(dataShift)
            print ("CRC Eq: C{} = {}".format(itemNum, dataShift[k]))
            crcEqList.append(dataShift[k])
            itemNum = itemNum-1
        self.equationList = crcEqList

        print("\n\n")
        self.equationListStr = []
        equationListStr = []
        for k,eq in enumerate(crcEqList):
            #print("{} {}".format(crcLen-k,eq))
            equationListStr = "C{} = ".format(crcLen-k)
            for m in eq:
                equationListStr = equationListStr + m.split("_")[0]+m.split("_")[1] + self.XOR
            self.equationListStr.append(equationListStr)

        for eq in self.equationListStr:
            print(eq)

        itemNum = 0
        # build the CRC Matrix to calculate the test vector CRC
        for k in crcEqList:
            # first number is the index of the equation
            self.equMatrix.append([itemNum])
            for j in k:
                #each item indicates the lcation and if its data or CRC word
                if (j.split('_')[0]=='c'):
                    itemListID = 0
                else:
                    itemListID = 1
                itemListIndex= j.split('_')[1]
                #print(j.split('_')[1])
                self.equMatrix[itemNum].append([itemListID,itemListIndex])
            itemNum = itemNum + 1

        #print(self.equMatrix)

    def makeShiftRegList(self,dataWidth):
        initValue = self.initValue
        crcLen = self.crcLen
        dataList=[]
        numList=[]
        cn = []
        dn = []

        # make datalist with LSB of each word first
        # bit 0 of the list is the LSB of the first word
        # the first CRC-Len are initialezed to the init value [0,1]
        for i in range(crcLen+1):
            cn.append(["c_"+str(i)])

        dataList = cn[::-1]

        for num in range(dataWidth):
            dn.append(["d_"+str(num)])

        for item in dn[::-1]:
            dataList.append(item)

        return dataList

    def makeTestList(self,dataWidth):
        #testInputList = ['0x1234', '0x5678', '0x2222', '0x2222', '0x333', '0x33333']
        #testInputList = ['0x3131', '0x3131', '0x3232', '0x3232', '0x3333', '0x3333']
        #testInputList = ['0x3131', '0x3131']
        #testInputList = ['0x4100', '0x0000']

        # Mesage: 'A'
        #testInputList = ['0x41', '0x00', '0x00']
        #testInputList = ['0x41']
        #testInputList = ['0xA', '0xA','0xB','0xA','0x0']

        #testInputList = ['0xff', '0xff', '0x31', '0x32', '0x33', '0x34', '0x35', '0x36', '0x37', '0x38', '0x39', '0x00', '0x00']
        testInputList = ['0x31', '0x32', '0x33', '0x34', '0x35', '0x36', '0x37', '0x38', '0x39', '0x00', '0x00']
        #testInputList = ['0xff', '0xff', '0x31', '0x32', '0x33', '0x34', '0x35', '0x36', '0x37', '0x38', '0x39', '0x00', '0x00', '0x00']
        #testInputList = ['0xffff', '0x3132', '0x3334', '0x3536', '0x3738', '0x3900', '0x0000']

        #testInputList = ['0x11', '0x11']

        #testInputList = ['0x00', '0x00']
        #testInputList = ['0x4100']
        #testInputList = ['0x0000', '0x0000']

        #a = str(testInputList[0])
        #a = testInputList[0]
        #b = a.split('0x')[1]
        #print (b)
        #print(b.__len__())
        #print(b[3])

        initValue = self.initValue
        crcLen = self.crcLen
        dataBitList=[]
        numList=[]
        self.testListNum = testInputList.__len__()
        self.testWordList = testInputList
        # make dataBitList with LSB of each word first
        # bit 0 of the list is the LSB of the first word
        # the first CRC-Len are initialezed to the init value [0,1]
        for i in range(crcLen+1):
            dataBitList.append(initValue)
        #print(format(5, '0>4b'))
        #for i in range(b.__len__()-1,-1,-1):
        for num in testInputList:
            b = num.split('0x')[1]
            bInt = int(b,16)
            for i in range(dataWidth):
                #print(i)
                numList.append(bInt%2)
                bInt=int(bInt/2)
            numList = numList[::-1]
            dataBitList = dataBitList + numList
            numList = []
        #print(dataBitList)
        #print(len(dataBitList))
        return dataBitList

    def calcCRC(self):
        crcLen = self.crcLen
        initValue = self.initValue
        testDataList = self.makeTestList(self.dataW)
        #print(testDataList)
        dataShift = testDataList
        for i in range(testDataList.__len__()-crcLen-1):
            #first Rshift then XOR
            for j in range(dataShift.__len__()-1):
                dataShift[j] = dataShift[j+1]
            dataShift[-1] = 9

            if dataShift[0]:
                for j in range(crcLen+1):
                    dataShift[j] = dataShift[j] ^ self.polyList[j]
        #print(dataShift)
        crc = hex(self.List2Val(dataShift,crcLen+1))
        crc = crc.split('0x')[1]
        print("Serial Calc CRC: {}\n".format(crc))
        return crc

    def calcCRCPar(self):
        crcLen = self.crcLen
        initValue = self.initValue
        testDataList = self.makeTestList(self.dataW)
        self.calcCRCEqu()
        #print("\ntestDataList: \n{}\n".format(testDataList))

        #make CRC Equations
        c = []
        d = []
        for i in range(crcLen + 1):
            c.append(initValue)

        for word in self.testWordList:
            d = []
            b = word.split('0x')[1]
            bInt = int(b,16)
            for i in range(self.dataW):
                #print(i)
                d.append(bInt%2)
                bInt=int(bInt/2)
            d = d[::-1]

            # calculate the Parallel CRC
            cd=[]
            cd.append(c[:])
            cd.append(d[:])
            for i in self.equMatrix:
                aXor = 0
                cBit = i[0]
                for j in range(1,i.__len__()):
                    aRow = i[j][0]
                    if (aRow == 0):
                        aCol = crcLen-int(i[j][1])
                    else:
                        aCol = (self.dataW-1)-int(i[j][1])

                    aXor = aXor ^ cd[aRow][aCol]
                c[cBit] = aXor

        crc = hex(self.List2Val(c,crcLen+1))
        crc = crc.split('0x')[1]
        print("Parallel Test CRC: {}".format(crc))
        return crc

    def List2Val(self,listIn,N):
        listVal = 0
        pow2 = 1
        listTrunc = listIn[1:N]
        listInv = listTrunc[::-1]
        # for i in range(N-1):
        #     listVal = listVal+pow2*listInv[i]
        #     pow2 = 2*pow2
        for i in listInv:
            listVal = listVal+pow2 * i
            pow2 = 2*pow2

        return listVal


#--------------
if __name__ == "__main__":

    # start the main code when called from console
    print(" CRC Calculator \n")

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


    #wordWidth = "32"
    print("Calling CRCParallel")
    CRC = CRCParallel(poly, 1, wordWidth) 
    #print(CRC.__doc__)
    #print(CRC.makeTestList())
    CRC.calcCRC()
    #print(CRC.makeShiftRegList(8))
    #CRC.calcCRCEqu(8)
    CRC.calcCRCPar()

    print("\n\n ==> Calling CRCParallel")
    CRC1 = CRCParallel('0x13', 0, 4)
    CRC1.calcCRC()
    CRC1.calcCRCPar()


    print("====end===")


       
       
      
    
        


    










 
      
    
        


    











