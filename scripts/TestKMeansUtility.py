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
                os.system("echo " + str(numClusters) + " clusters, " + \
                              str(numThread) + " threads, " + \
                              str(numSlices) + " slices >> " + \
                              finalOutputFile)  
                
                outputFileName = outputdir + "log-" + str(numThread) + "-" + str(numClusters) + "-" + str(numSlices)
                
                commandLineStr = "bin/run-example-with-threadNum " + str(numThread) \
                    + " org.apache.spark.examples.mllib.KMeansTest -k " + str(numClusters) + \
                    " --numIterations 10 --heapSize 5 --numSlices "+ str(numSlices) + \
                    " --useMultithreaded 0" + \
                    " 2>>" + outputFileName
                print commandLineStr
                os.system(commandLineStr)
                os.system("python ./scripts/parse-mxbeans-heap.py " + outputFileName + ">>" + finalOutputFile)
    os.chdir("./scripts")


def testMultithreaded(numThreadsArray, numClustersArray, numSlicesArray, numThreadsPerTaskArray):
    os.chdir("..")
    os.system("pwd")
    outputdir = "./logs/" + str(datetime.datetime.now()).replace(' ', '') +"/"
    os.mkdir(outputdir)
    numSlices = 4

    finalOutputFile = outputdir + "summary.out" 
    for numClusters in numClustersArray:
        for numThread in numThreadsArray:
            for numSlices in numSlicesArray:
                for numThreadsPerTask in numThreadsPerTaskArray:
        #os.system("echo " + str(numThread))          
                    os.system("echo " + str(numClusters) + " clusters, " + \
                                  str(numThread) + " threads, " + \
                                  str(numSlices) + " slices, multithreaded " + \
                                  "with " + str(numThreadsPerTask) + " threads per task >>" +\
                                  finalOutputFile)  
                    outputFileName = outputdir + "log-" + str(numThread) + "-" + str(numClusters) + \
                        "-" + str(numSlices) + "-multithreaded"
                    commandLineStr = "bin/run-example-with-threadNum " + str(numThread) + \
                        " org.apache.spark.examples.mllib.KMeansTest -k " + str(numClusters) + \
                        " --numIterations 10 --heapSize 5 --numSlices "+ str(numSlices) + \
                        " --numThreadsPerTask " + str(numThreadsPerTask) + \
                        " --useMultithreaded 1" + \
                        " 2>>" + outputFileName
                    print commandLineStr
                    os.system(commandLineStr)
                    os.system("python ./scripts/parse-mxbeans-heap.py " + outputFileName + ">>" + finalOutputFile)
    os.chdir("./scripts")

#test([6], [3000], [6])
#test([1], [1000, 2000, 3000], [6])
#test([2],[1000],[6])
#testMultithreaded([1, 2, 3],[2000, 3000, 4000],[2, 4, 6],[2, 4, 6])
#testMultithreaded([2],[2000],[6],[4])
