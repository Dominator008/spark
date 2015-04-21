
import sys

filename = sys.argv[1]
file = open(filename).read()
lines = [l.replace(':', ' ').replace(',', ' ').split(' ') for l in file.split('\n')[1:]]

HeapMemList = []
Iterations = ""
Time = ""

for line in lines:
    #print line
    for i in range(len(line)):
        if line[i] == 'Heap':
            #print line
            #print line[i+4]                                                    
            HeapMemList.append(int(line[i+8]))
        if line[i] == 'Iterations' and line[i+1] == 'took':
            print line
            Time = (line[i+2])
        if line[i] == 'finished' and line[i+1] == 'in' and line[i+3] == 'iterations':
            print line
            Iterations = (line[i+2])

            
#print HeapMemList
            
print "average heap mem utilization: " +  str(sum(HeapMemList)/(1024*1024*len(HeapMemList))) + " MB"
print "max heap mem utilization: " +  str(max(HeapMemList)/(1024*1024)) + " MB"
print "ran " + Iterations + " iterations for " + Time + " seconds"
