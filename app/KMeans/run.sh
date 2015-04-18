#!/bin/bash

sbt package
../../bin/spark-submit --class "KMeansTest" --master local[8] target/scala-2.10/kmeanstest_2.10-1.0.jar
