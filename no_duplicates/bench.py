#!/usr/bin/python

import sys, re, tempfile, os, tempfile, subprocess, simplejson

try:
    tests = filter(lambda x:re.match("[^#].*? # .*?", x), file("README").readlines())
except IOError:
    print "The README file is needed for the benchmarks."
    sys.exit(1)

try:
    import bitarray
except ImportError:
    print "You have to install the bitarray python module"
    sys.exit(1)

#generating testdata
testCases = zip([100000, 300000, 750000, 1500000, 3000000, 6000000, 13000000],
            ["/tmp/%s.txt"%x for x in ["100k", "300k", "750k", "1.5m", "3m", "6m", "13m"]])

for count, fn in testCases:
    if os.path.exists(fn):
        print "found generated %s - fine." % fn
    else:
        print "generating %d unique numbers -> %s" % (count, fn)
        os.system("python gen_random_numbers.py %d > %s" % (count, fn))

#create temp. filenames for output
timeOutName = tempfile.mktemp()
collect = dict([(str(x[0]), {}) for x in testCases])

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
        i = open(timeOutName)
        try:
            collect[str(lineCount)][source] = i.read().strip().split()
        finally:
            i.close()
            os.unlink(timeOutName)
        dataOut.close()

json={}
tests = sorted(collect.keys(), lambda a,b: int(a)-int(b))
scripts = sorted(collect["100000"].keys())
for i, chart in enumerate(["usertime in sec", "systemtime in sec", "max memory in kb"]):
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
        "data": [float(collect[test][script][i]) for test in tests]
                           })

print "generating charts.json for highcharts.com ..."
fp = file("charts.json", "w")
fp.write("var charts = "+simplejson.dumps(json)+";");
fp.close()
