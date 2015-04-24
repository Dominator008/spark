#!/bin/python
import csv
import locale
import sys

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

file = open(sys.argv[1])
file.readline()
reader = csv.reader(file)
count = 0
maxHeap = 0
sumHeap = 0
for r in reader:
  count += 1
  used = locale.atoi(r[2])
  sumHeap += used 
  maxHeap = used if used > maxHeap else maxHeap

print "Average heap utilization: " + str(sumHeap / count / (1024*1024.0)) + " MB"
print "Max heap utilization: " + str(maxHeap / (1024*1024.0)) + " MB"
