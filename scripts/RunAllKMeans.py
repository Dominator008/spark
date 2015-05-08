#!/bin/python

import datetime
import os
import threading
import time

def test(numThreadsArray, numClustersArray, numSlicesArray):
  os.chdir("..")
  outputdir = "./logs/" + str(datetime.datetime.now()).replace(' ', '') +"/"
  os.mkdir(outputdir)
  numSlices = 4
  finalOutputFile = outputdir + "summary.out"
  for numClusters in numClustersArray:
    for numThread in numThreadsArray:
      for numSlices in numSlicesArray:
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
        sparkThread = threading.Thread(target = os.system, args = (commandLineStr,))
        sparkThread.daemon = True
        sparkThread.start()
        time.sleep(2)
        jstatRaw = outputdir + "jstatRaw.csv"
        jstatCommand = "jstat -gc `jps -l | grep SparkSubmit | awk {'print $1'}` 1000" + ">" + jstatRaw
        os.system(jstatCommand)
        os.system("python ./scripts/parse-mxbeans-heap.py " + outputFileName + ">>" + finalOutputFile)
        os.system("python ./scripts/parse-jstat-heap.py " + jstatRaw + ">>" + finalOutputFile)

  os.chdir("./scripts")


def testMultithreaded(numThreadsArray, numClustersArray, numSlicesArray, numThreadsPerTaskArray):
  os.chdir("..")
  outputdir = "./logs/" + str(datetime.datetime.now()).replace(' ', '') +"/"
  os.mkdir(outputdir)
  numSlices = 4

  finalOutputFile = outputdir + "summary.out"
  for numClusters in numClustersArray:
    for numThread in numThreadsArray:
      for numSlices in numSlicesArray:
        for numThreadsPerTask in numThreadsPerTaskArray:
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
          sparkThread = threading.Thread(target = os.system, args = (commandLineStr,))
          sparkThread.daemon = True
          sparkThread.start()
          time.sleep(2)
          jstatRaw = outputdir + "jstatRaw.csv"
          jstatCommand = "jstat -gc `jps -l | grep SparkSubmit | awk {'print $1'}` 1000" + ">" + jstatRaw
          os.system(jstatCommand)
          os.system("python ./scripts/parse-mxbeans-heap.py " + outputFileName + ">>" + finalOutputFile)
          os.system("python ./scripts/parse-jstat-heap.py " + jstatRaw + ">>" + finalOutputFile)
  os.chdir("./scripts")

#test([6], [3000], [6])
#test([1], [1000, 2000, 3000], [6])
test([8],[1000, 3000, 5000],[8])
test([10],[1000, 3000, 5000],[10])
testMultithreaded([2],[1000, 3000, 5000],[6],[6])
testMultithreaded([3],[1000, 3000, 5000],[4],[4])
testMultithreaded([3],[1000, 3000, 5000],[6],[6])
#testMultithreaded([2, 4],[6000],[2, 4],[2, 4])
