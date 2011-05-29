#!/usr/bin/python
'''
read unsorted numbers (one each line) and filter the
doubles out. this variant sort only sub-ranges and merge 
the sub-parts with heapq.

This code is not memory-optimized (like the array.array
byte-efficient list module).


'''
import sys, tempfile, heapq

limit = 50000
if len(sys.argv)>1:
    limit = int(sys.argv[1])

def fileIterator(digits):
    fp = tempfile.TemporaryFile()
    fp.write("\n".join(map(lambda x:str(x), sorted(digits))))
    fp.seek(0)
    return fp

iters = []
digits = []
for line in sys.stdin:
    digits.append(int(line.strip()))
    if len(digits)==limit:
        iters.append(fileIterator(digits))
        digits = []
iters.append(fileIterator(digits))

#merge all sorted ranges and filter doubles
oldItem = -1
for sortItem in heapq.merge(*iters):
    if oldItem != sortItem:
        print "%s" % sortItem.strip()
    oldItem = sortItem
