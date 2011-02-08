import random
limit = 13000000
start = 1000000
stop  = 100000000


#generate 99% random digits without doubles
digits = set()
count = limit * 99 / 100
while count:
  d = random.randint(start, stop)
  if d not in digits:
      digits.add(d)
      count-=1

#add 1% doubles to the list of digits
myList = list(digits)
for x in range(limit/100):
    myList.append(random.choice(myList))

for digit in myList:
    print digit
