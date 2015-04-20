package org.apache.spark.examples.mllib

import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import scala.io.Source._

object KMeansTest {

  def main(args: Array[String]) {

    val conf = new SparkConf().setAppName("KMeans")
        .set("spark.executor.extraJavaOptions", "-XX:+PrintGC")
    val sc = new SparkContext(conf)

    // Load and parse the data
    //val data = sc.textFile("/Users/yunmingzhang/Documents/Research/spark/data/mllib/kmeans_data.txt")
    // val data = sc.textFile("data/mllib/kmeans_data.txt")
    // val parsedData = data.map(s => Vectors.dense(s.split(' ').map(_.toDouble))).cache()

    val indexLines = fromFile("data/mllib/kmeans_index.txt").getLines
    val valLines = fromFile("data/mllib/kmeans_val.txt").getLines
    val sparseVectorList = scala.collection.mutable.Buffer[org.apache.spark.mllib.linalg.Vector]()
    val length = 15000 //number of unique words, hard coded length of the sparse vector

    while (indexLines.hasNext) {
        val indexArray = indexLines.next().split(' ').map(_.toInt)
        val valArray = valLines.next().split(' ').map(_.toDouble)
        val sparseVector = Vectors.sparse(length, indexArray, valArray)
        sparseVectorList += sparseVector
    }

    val sparseVectorListRDD = sc.parallelize(sparseVectorList)

    // Cluster the data into two classes using KMeans
    val numClusters = 30
    val numIterations = 40

    val clusters = KMeans.train(sparseVectorListRDD, numClusters, numIterations)

    // Evaluate clustering by computing Within Set Sum of Squared Errors
    val WSSSE = clusters.computeCost(sparseVectorListRDD)
    println("Within Set Sum of Squared Errors = " + WSSSE)

    }
}
