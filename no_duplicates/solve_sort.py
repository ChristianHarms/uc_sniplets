import sys

last = ""
for n in sorted(open(sys.argv[1])):
    if last != n:
        sys.stdout.write( n )
    last = n
