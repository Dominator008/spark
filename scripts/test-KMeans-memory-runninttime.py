#!/bin/python

import os
import datetime

def test(numThreadsArray, numClustersArray):
    os.chdir("..")
    os.system("pwd")
    finalOutputFile = "test-out-" + str(datetime.datetime.now()).replace(' ', '') 
    for numClusters in numClustersArray:
        for numThread in numThreadsArray:
        #os.system("echo " + str(numThread))
            outputFileName = "log-" + str(numThread) + "-" + str(numClusters)
            commandLineStr = "bin/run-example-with-threadNum " + str(numThread) + " org.apache.spark.examples.mllib.KMeansTest -k " + str(numClusters) + " --numIterations 15 --heapSize 5 --numSlices 20 2>" + outputFileName
            print commandLineStr
            os.system(commandLineStr)
            os.system("python ./scripts/parse-mxbeans-heap.py " + outputFileName + ">>" + finalOutputFile)

test([1, 2, 4, 8, 12], [1000, 1500, 2000])
