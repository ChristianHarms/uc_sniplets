import sys
from bitarray import bitarray
minValue = 1000000
maxValue = 100000000
bits = bitarray(maxValue-minValue+1)
 
for line in file(sys.argv[1]):
   i = int(line)
   if not bits[i - minValue]:
       bits[i - minValue] = 1
       sys.stdout.write(line)
