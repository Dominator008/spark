#!/bin/python

import os
import datetime

def test(numThreadsArray, numClustersArray, numSlicesArray):

    os.chdir("..")
    os.system("pwd")
    outputdir = "./logs/" + str(datetime.datetime.now()).replace(' ', '') +"/"
    os.mkdir(outputdir)
    numSlices = 4

    finalOutputFile = outputdir + "summary.out"
    for numClusters in numClustersArray:
        for numThread in numThreadsArray:
            for numSlices in numSlicesArray:
        #os.system("echo " + str(numThread))          
                os.system("echo " + str(numClusters) + " clusters, " + str(numThread) + " threads, " + str(numSlices) + " slices >> " + finalOutputFile)  
                outputFileName = outputdir + "log-" + str(numThread) + "-" + str(numClusters) + "-" + str(numSlices)
                commandLineStr = "bin/run-example-with-threadNum " + str(numThread) + " org.apache.spark.examples.mllib.KMeansTest -k " + str(numClusters) + " --numIterations 10 --heapSize 5 --numSlices "+ str(numSlices) + " 2>>" + outputFileName
                print commandLineStr
                os.system(commandLineStr)
                os.system("python ./scripts/parse-mxbeans-heap.py " + outputFileName + ">>" + finalOutputFile)

#test([1, 2, 4, 8, 12], [1000, 1500, 2000])
#test([2, 4, 6], [1000, 2000], [6,8])
test([6],[1000],[6])
