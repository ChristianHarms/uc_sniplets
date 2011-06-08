#!/usr/bin/python

import sys, re, tempfile, os, tempfile, subprocess, simplejson
simplejson.encoder.FLOAT_REPR = lambda f: ("%.5f" % f)

try:
    tests = filter(lambda x:re.match("[^#].*? # .*?", x), file("README").readlines())
except IOError:
    print "The README file is needed for the benchmarks."
    sys.exit(1)

print "Checking interpreter and needed commands ..."
for cmd in ["lua", "gcc", "python", "perl"]:
    if os.system("which %s" % cmd):
        print "%s is not in your path - install it" % cmd
        sys.exit(1)

print "Checking needed python module ..."
try:
    import bitarray
except ImportError:
    print "You have to install the bitarray python module"
    sys.exit(1)


#generating testdata, starting from 1 million to 13 million
testCases = [(int(i * 1e6),"/tmp/%dm.txt"%i) for i in range(1,6)]

for count, fn in testCases:
    if os.path.exists(fn):
        print "found generated %s - fine." % fn
    else:
        print "generating %d unique numbers -> %s" % (count, fn)
        os.system("python gen_random_numbers.py %d > %s" % (count, fn))

#create temp. filenames for output
timeOutName = tempfile.mktemp()
collect = dict([(x[0], {}) for x in testCases])

for test in tests:
    source, desc = re.split("\s+#\s+", test)
    runner = ""

    #compile the c source
    if source.strip().endswith(".c"):
        runner = "./" + source.strip(".c")
        if os.path.exists(runner):
            os.unlink(runner)
        print "Compiling %s with gcc ..." % source
        os.system("gcc -O5 -o %s %s" % (runner, source))
        if not os.path.exists(runner):
            print "Problem with compiling #%s#" % ("gcc -O5 -o %s %s" % (runner, source))
            break

    #inject the python source with the interpreter    
    if source.strip().endswith(".py"):
        runner = "python %s" % source

    #inject the lua source with the interpreter    
    if source.strip().endswith(".lua"):
        runner = "lua %s" % source

    runner = runner or source
    print "RUNNER:%s ..." % runner

    #build the command line with time
    cmd = "/usr/bin/time --format=\"%%S %%U %%M\" --output=%s %s"  % (timeOutName, runner)

    #run the test code with the different input files
    for (lineCount, dataInName) in testCases:
        cmdTest = "%s %s" % (cmd, dataInName)

        #only the qsort-C variant need the line count as parameter
        if cmdTest.find("qsort")!=-1:
            cmdTest += " %d" % lineCount

        dataOutName = tempfile.mktemp()
        print "> %s >%s " % (cmdTest, dataOutName)
        dataOut = file(dataOutName, "w")
        errCode = subprocess.Popen(cmdTest, stdout=dataOut, shell=True).wait()
        #print "errCode: %d" % errCode
        input = open(timeOutName)
        try:
            collect[lineCount][source] = map(float, input.read().strip().split())
            collect[lineCount][source][2]/=1024 #saving MB, not KB
        finally:
            input.close()
            os.unlink(timeOutName)
        dataOut.close()

json={}
tests = sorted(collect.keys(), lambda a,b: int(a)-int(b))
scripts = sorted(collect[testCases[0][0]].keys())
for i, chart in enumerate(["usertime in sec", "systemtime in sec", "max memory in MB"]):
  json[str(i)] = {"xAxis": {"categories": tests , "title": {"text": "count of numbers"}}, 
                  "yAxis": {"title":{"text":chart}},
                  "chart": {"renderTo": "chart%d"%i, "defaultSeriesType": 'spline'},
                  "series": [],
                  #"legend": { "layout": 'vertical',
                  #            "align": 'right',
                  #            "verticalAlign": 'top',
                  #            "x": -10,
                  #            "y": 100,
                  #            "borderWidth": 0
                  #            },
                  "title": { "text": chart }
                  }

  for script in scripts:
    json[str(i)]['series'].append({"name": script,
        "data": [collect[test[0]][script][i] for test in testCases]
                           })

print "generating charts.js for highcharts.com ..."
fp = file("charts.js", "w")
fp.write("var charts = "+simplejson.dumps(json)+";");
fp.close()
