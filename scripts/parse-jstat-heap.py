#!/bin/python
import csv
import sys

file = open(sys.argv[1])
file.readline()
reader = csv.reader(file, delimiter = ' ', skipinitialspace = True)
count = 0
maxHeap = 0
sumHeap = 0
for r in reader:
  count += 1
  used = float(r[2]) + float(r[3]) + float(r[5]) + float(r[7])
  sumHeap += used
  maxHeap = used if used > maxHeap else maxHeap

print "Average heap utilization: " + str(sumHeap / count / 1024) + " MB"
print "Max heap utilization: " + str(maxHeap / 1024) + " MB"
