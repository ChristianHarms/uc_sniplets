import sys

values = map(int, open(sys.argv[1]))
values.sort()

last = 0
for n in values:
    if last != n:
        sys.stdout.write("%d\n" % n)
    last = n
