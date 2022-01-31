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

#print ('Hello, world!')

#####################################
## Functions
#####################################
def makePolyList(poly):
    crcPolyHexInput = int(poly)  # CRC-32
    crcPolyShift = int(crcPolyHexInput)

    equationList = []

    # make the list-array for the poly
    crcLen = 0

    while crcPolyShift > 0:
        polyList.append(crcPolyShift % 2)
        crcPolyShift = int(crcPolyShift / 2)
        crcList.append('c' + str(crcLen))
        equationList.append('c' + str(crcLen) + ' = ')
        crcLen = crcLen + 1

    # remove the '1' in the MSB of the polyList.
    # it's always '1' and will cause complication further.
    print(polyList)
    polyList[crcLen - 1] = 0

    return polyList




#####################################
sampData = [1, 1, 0, 1, 1, 0, 0, 1]

#dataW = 4
dataW = 32

XOR = ' ^ '
crcPolyHexInput = int(0x19) # 11001 CRC-4
crcPolyHexInput = int(0x100050003) # CRC-32

crcPolyShift = int(crcPolyHexInput)

polyList = []
crcList  = []
dataList = []
equationList = []
crcLen = 0

for i in range(dataW):
    dataList.append('d'+str(i))
    i = i+1

##-#  # make the list-array for the poly
##-#  crcLen = 0
##-#  while crcPolyShift > 0:
##-#      polyList.append(crcPolyShift %2)
##-#      crcPolyShift = int(crcPolyShift/2)
##-#      crcList.append('c'+str(crcLen))
##-#      equationList.append('c'+str(crcLen)+' = ')
##-#      crcLen = crcLen+1
##-#
##-#  # remove the '1' in the MSB of the polyList.
##-#  # it's always '1' and will cause complication further.
##-#  print(polyList)
##-#  polyList[crcLen-1] = 0

polyList = makePolyList(0x100050003)

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











