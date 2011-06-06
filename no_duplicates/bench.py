#!/usr/bin/python

import sys, re, tempfile, os, tempfile, subprocess

try:
    tests = filter(lambda x:re.match("[^#].*? - .*?", x), file("README").readlines())
except IOError:
    print "The README file is needed for the benchmarks."
    sys.exit(1)

try:
    import bitarray
except ImportError:
    print "You have to install the bitarray python module"
    sys.exit(1)

#generating testdata
testCases = zip([100000, 400000, 1300000],#, 4000000, 1300000],
            ["/tmp/%s.txt"%x for x in ["100k", "400k", "1.3m"]])#, "4m"]])

for count, fn in testCases:
    if os.path.exists(fn):
        print "found generated %s - fine." % fn
    else:
        print "generating %d unique numbers -> %s" % (count, fn)
        os.system("python gen_random_numbers.py %d > %s" % (count, fn))

#create temp. filenames for output
timeOutName = tempfile.mktemp()
dataOutName = tempfile.mktemp()

for test in tests:
    source, desc = test.split(" - ")

    #prepare the test code
    if source.endswith(".c"):
        if os.path.exists("a.out"):
            os.unlink("a.out")
        print "Compiling %s with gcc ..." % source
        os.system("gcc -O5 %s" % source)
        if not os.path.exists("a.out"):
            print "Problem with compiling %s" % source
            break
        source = "./a.out"
    if source.endswith(".py"):
        source = "python %s" % source
    cmd = "/usr/bin/time --output=%s %s"  % (timeOutName, source)

    #run the test code with the different input files
    for (lineCount, dataInName) in testCases:
        cmdList = cmd.split() + [str(lineCount)]
        print "> %s %d <%s >%s " % (cmd, lineCount, dataInName, dataOutName)
        dataOut = file(dataOutName, "w")
        sourceIn = file(dataInName)
        subprocess.Popen(cmdList, stdout=dataOut, stdin=sourceIn).wait()
        i = open(timeOutName)
        try:
            match = re.search("(\d+\.\d+)user (\d+\.\d+)system.*?(\d+)maxresident", i.read(), re.S)
            if match:
                print match.groups()
        finally:
            i.close()
            os.unlink(timeOutName)
        dataOut.close()
        sourceIn.close()
