import sys

last = ""
for line in sorted(open(sys.argv[1])):
    if last != line:
        sys.stdout.write(line)
    last = line
