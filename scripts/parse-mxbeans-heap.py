
import sys

filename = sys.argv[1]
file = open(filename).read()
lines = [l.replace(',', ':').split(':') for l in file.split('\n')[1:]]

HeapMemList = []

for line in lines:
    for i in range(len(line)):
        if line[i] == ' Heap':
            #print line
            #print line[i+4]                                                    
            HeapMemList.append(int(line[i+4]))
            
#print HeapMemList
            
print "average heap mem utilization: " +  str(sum(HeapMemList)/(1024*1024*len(HeapMemList))) + " MB"
print "max heap mem utilization: " +  str(max(HeapMemList)/(1024*1024)) + " MB"
