import sys
from bitarray import bitarray
LOW = 1000000
HIGH = 100000000
v = bitarray(HIGH-LOW+1)
 
for line in file(sys.argv[1]):
   i = int(line)
   if not v[i - LOW]:
       v[i - LOW] = 1
       print i
