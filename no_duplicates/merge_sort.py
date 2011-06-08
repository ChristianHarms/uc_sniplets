#!/usr/bin/python
'''
read unsorted numbers (one each line) and filter the
doubles out. this variant sort only sub-ranges and merge 
the sub-parts with heapq.

'''
import sys, tempfile, heapq

limit = 40000

def sortedFileIterator(digits):
    fp = tempfile.TemporaryFile()
    digits.sort()
    fp.write("\n".join(map(lambda x:str(x), digits)))
    fp.seek(0)
    return fp

iters = []
digits = []
for line in file(sys.argv[1]):
    digits.append(int(line.strip()))
    if len(digits)==limit:
        iters.append(sortedFileIterator(digits))
        digits = []
iters.append(sortedFileIterator(digits))

#merge all sorted ranges and filter doubles
oldItem = -1
for sortItem in heapq.merge(*iters):
    if oldItem != sortItem:
        print sortItem.strip()
    oldItem = sortItem
