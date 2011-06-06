import sys

for n in set(open(sys.argv[1])):
    sys.stdout.write( n )
