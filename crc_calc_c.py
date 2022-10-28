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
        #self.polyInv = poly.reverse()
        #self.polyInv = poly[::-1]

        # make the poly to a HEX number
        self.crcPolyHexInput = int(poly, base=16)
        #self.crcPolyHexInput = poly
        #self.wordWidth = wordWidth
        self.dataW = int(wordWidth)
        self.polyList = []
        self.polyListInv = []
        self.crcList  = []
        #self.crcListInd  = []
        #self.dataList = []
        self.testListNum = 0
        self.equationList = []
        self.equMatrix = []
        self.cn = []
        self.dn = []
        self.XOR = ' ^ '
        #self.crcMatrix = [][]
        #self.testInput = ['0x1234', '0x5678', '0x9abc', '0xdefc']
        #self.testCRC = 0
        self.crcLen = 0
        #print('new CRC instance')
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

        self.polyList = polyList[::-1]
        polyListInv = polyList[::-1]
        #self.polyListInv = polyListInv[1::]
        self.polyListInv = polyListInv
        self.crcLen = polyList.__len__()-1
        self.polyListInv = self.polyListInv + [0]*(self.dataW)
        print("poly: {}; order: {}; polyList: \n{}".format(self.poly, self.crcLen, self.polyList))

    def makeDataList(self):
        # make the list to hold the data inputs
        for i in range(self.dataW):
            #self.dataList.append('d' + str(i))
            self.dn.append('d' + str(i))
            #self.dn.append(self.dataList[i])
        print("dn: {}".format(self.dn))



    def makeCrcList(self):
        for i in range(self.crcLen):
            self.crcList.append('c' + str(i))
        self.crcList = self.crcList[::-1]
        self.crcList = self.crcList + self.dn
        print("crcList: {}".format(self.crcList))

            #self.crcListInd.append([self.crcList[i]])
            #self.cn.append(i)


    def crcCalcEquation(self):
        self.makeDataList()
        self.makeCrcList()

        print("polyList:    {}".format(self.polyList))
        print("polyListInv: {}".format(self.polyListInv))
        print("crcLen: {}".format(self.crcLen))

        # remove the '1' in the MSB of the polyList. - change to no remove
        # it's always '1' and will cause complication further.
        #print(self.polyList)
        #self.polyList[self.crcLen-1] = 0
        self.polyListInv[0] = 0

        # start the equation calc
        #print("crcList:    {}".format(self.crcList))
        #print("crcListInd: {}".format(self.crcListInd))
        #print("cn: {}".format(self.cn))
        #print("dn: {}".format(self.dn))
        #print("crcLen: {}".format(self.crcLen))

        # make the shift process
        # shift over the current CRC register for the dataW cycles
        # each step set the XOR bits according to the poly 
        for i in range(self.dataW):
            cHigh = self.crcList[0]
            for j in range(self.crcList.__len__()-1): # in range(self.crcLen):
                if self.polyListInv[j]==1:
                    self.crcList[j] = cHigh + self.XOR + self.crcList[j+1]
                else:
                    self.crcList[j] = self.crcList[j+1]
            self.crcList[-1] = 'X'
            # now move-in the next data
            #if self.polyList[0] == 1:
            #    self.crcList[0] = cHigh + self.XOR + self.dn[i]
            #else:
            #    self.crcList[0] = self.dn[i]

        crcLisrSplit = []
        for i in self.crcList[0:self.crcLen]:
            crcLisrSplit.append(i.split(self.XOR))
        print("crcLisrSplit: {}".format(crcLisrSplit))
        #crcLisrSplit = crcLisrSplit[]

        # remove dulplicate items (as b^a^a^c = b^c)

        crcLisrSplit = crcLisrSplit[::-1]

        for cn in crcLisrSplit:
            removeList = []
            print("cn a: {}".format(cn))
            cn.sort()
            print("cn b: {}".format(cn))
            print(len(cn))

            removeCnt = 0
            for i in range(1,len(cn)):
                if (cn[i-1] == cn[i]):
                    cn[i-1] = 'x'
                    cn[i] = 'x'
                    removeCnt = removeCnt+2
                    #removeList.append(cn[i-1])
                    #removeList.append(cn[i])
            for k in range(removeCnt):
                cn.remove('x')
            #for k in removeList:
            #    cn.remove(k)

            print("cn c: {}".format(cn))
            print("-----------------------")


        for i in range(self.crcLen):
            self.equationList.append('c'+str(i)+' = ' + crcLisrSplit[i][0])

        for i in range(len(self.equationList)):
            for j in range(1, len(crcLisrSplit[i])):
                self.equationList[i] = self.equationList[i] + self.XOR + crcLisrSplit[i][j]

        for i in self.equationList:
            print(i)


    def crcCalcEquation0(self):
        crcPolyShift = self.crcPolyHexInput

        self.makeDataList()

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

    def calcCRCEqu(self,dataWidth):
        crcLen = self.crcLen
        dataList = self.makeShiftRegList(dataWidth)
        crcEqList = []

        #print(dataList)
        dataShift = dataList[:]

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
        k = 0
        for i in dataShift:
            for j in i:
                #print(i.count(j))
                if (i.count(j)>1):
                    print("Clean list for: ({}): {}, {} x {}".format(k, i, i.count(j), j))
                    i.remove(j)
                    i.remove(j)
            k = k+1

        itemNum = crcLen
        #for k in range(crcLen,-1,-1): #enumerate(dataShift)
        for k in range(crcLen+1):  # enumerate(dataShift)
            print ("CRC Eq: C{} = {}".format(itemNum, dataShift[k]))
            crcEqList.append(dataShift[k])
            itemNum = itemNum-1
        self.equationList = crcEqList

        itemNum = 0
        itemListID = 0
        itemListIndex = 0

        for k in crcEqList:
            self.equMatrix.append([itemNum])
            for j in k:
                if (j.split('_')[0]=='c'):
                    itemListID = 0
                else:
                    itemListID = 1
                itemListIndex= j.split('_')[1]
                #self.equMatrix[itemNum].append(j.split('_')[1])
                #print(j.split('_')[1])
                self.equMatrix[itemNum].append([itemListID,itemListIndex])
            itemNum = itemNum + 1

        #print(self.equMatrix)







        #crc = hex(self.List2Val(dataShift,17))
        #crc = crc.split('0x')[1]
        #print("CRC: {}".format(crc))


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
        testInputList = ['0x41']

        #testInputList = ['0xff', '0xff', '0x31', '0x32', '0x33', '0x34', '0x35', '0x36', '0x37', '0x38', '0x39', '0x00', '0x00']
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

    def makeGolden(self):
        data = self.makeTestList()
        print("makeGolden: data: {}".format(data))
        for shift in range(len(data)-17):
            for d in range(len(data)-1):
                data[d] = data[d+1]
            data[-1]=8
            if (data[0]==1):
                for j in range(self.polyList.__len__()):
                    data[j] = data[j] ^ self.polyList[j]

            print(data)
            print(self.polyList)

    def calcCRC(self,dataWidth):
        crcLen = self.crcLen
        initValue = self.initValue
        testDataList = self.makeTestList(dataWidth)
        print(testDataList)
        dataShift = testDataList
        for i in range(testDataList.__len__()-crcLen-1):
            #first Rshift then XOR
            for j in range(dataShift.__len__()-1):
                dataShift[j] = dataShift[j+1]
            dataShift[-1] = 9

            if dataShift[0]:
                for j in range(crcLen+1):
                    dataShift[j] = dataShift[j] ^ self.polyList[j]
        print(dataShift)
        crc = hex(self.List2Val(dataShift,17))
        crc = crc.split('0x')[1]
        print("CRC: {}".format(crc))

    def calcCRCPar(self,dataWidth):
        crcLen = self.crcLen
        initValue = self.initValue
        testDataList = self.makeTestList(dataWidth)
        self.calcCRCEqu(8)
        print(testDataList)

        #make CRC reg
        c = []
        d = []
        for i in range(crcLen + 1):
            c.append(initValue)

        for word in self.testWordList:
            d = []
            b = word.split('0x')[1]
            bInt = int(b,16)
            for i in range(dataWidth):
                #print(i)
                d.append(bInt%2)
                bInt=int(bInt/2)
            d = d[::-1]

            # calculate the Parallel CRC
            cd=[]
            cd.append(c[:])
            cd.append(d[:])
            for i in self.equMatrix:
                cBit = i[0]
                for j in range(1,i.__len__()):
                    aRow = i[j][0]
                    if (aRow == 0):
                        aCol = 16-int(i[j][1])
                    else:
                        aCol = 7-int(i[j][1])
                    c[cBit] = c[cBit] ^ cd[aRow][aCol]


        crc = hex(self.List2Val(c,17))
        crc = crc.split('0x')[1]
        print("CRC: {}".format(crc))


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



    #def hex2bin(self, x):


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

    CRC = CRCParallel(poly, 1, wordWidth)
    #print(CRC.__doc__)
    #CRC.crcCalcEquation()
    #CRC.makeGolden()
    #print(CRC.makeTestList())
    ##CRC.makeGolden()
    CRC.calcCRC(8)
    #print(CRC.makeShiftRegList(8))
    #CRC.calcCRCEqu(8)
    CRC.calcCRCPar(8)
    print("====end===")

    #CRC4 = CRCParallel('0x1001', 8)
    #CRC4.crcCalcEquation()
    
       
       
      
    
        


    










 
      
    
        


    











