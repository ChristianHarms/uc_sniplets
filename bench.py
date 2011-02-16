#!/usr/bin/python

import sys, re, tempfile, os

try:
    tests = filter(lambda x:re.match(".*? - .*?", x), file("README").readlines())
except IOError:
    print "The README file is needed for the benchmarks."
    sys.exit(1)

try:
    import bitarray
except ImportError:
    print "You have to install the bitarray python module"
    sys.exit(1)

#generating testdata
lines = zip([100000, 600000, 1300000, 6000000, 130000000],
            ["/tmp/%s.txt"%x for x in ["100k", "600k", "1.3m", "6m", "13m"]])

for count, fn in lines:
    if os.path.exists(fn):
        print "found generated %s - fine." % fn
    else:
        print "generating %d unique numbers -> %s" % (count, fn)
        os.system("python gen_random_numbers.py %d > %s" % (count, fn))


for test in tests:
    source, desc = test.split(" - ")

    if source.endswith(".c"):
        if os.path.exists("a.out"):
            os.path.unlink("a.out")
        os.system("gcc -O5 %s" % source)
        if not os.path.exists("a.out"):
            print "Problem with compiling %s" % source
            break
        for count, fn in lines:
            print "/usr/bin/time %s <%s >result.txt " % (source, fn)
