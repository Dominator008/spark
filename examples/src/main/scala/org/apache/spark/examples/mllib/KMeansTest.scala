package org.apache.spark.examples.mllib

import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import scala.io.Source._
import scopt.OptionParser

object KMeansTest {

    case class Params (
        k: Int = 30,
        numIterations: Int = 10,
        heapSize: Int = 8,
        numSlices: Int = 16) extends AbstractParams[Params]
    


    def main(args: Array[String]) {

        
        val defaultParams = Params()
        val parser = new OptionParser[Params]("KMeansTest") {
          head("KMeansTest: an example k-means app for dense data.")
          opt[Int]('k', "k")
            .required()
            .text(s"number of clusters, required")
            .action((x, c) => c.copy(k = x))
          opt[Int]("numIterations")
            .required()
            .text(s"number of iterations, default: ${defaultParams.numIterations}")
            .action((x, c) => c.copy(numIterations = x))
          opt[Int]("heapSize")
            .required()
            .text(s"heap size (GB), required")
            .action((x, c) => c.copy(heapSize = x))
          opt[Int]("numSlices")
            .required()
            .text(s"hnumSlices, required")
            .action((x, c) => c.copy(heapSize = x))
        }

         parser.parse(args, defaultParams).map { params =>
          run(params)
        }.getOrElse {
          sys.exit(1)
        }


    }

    def run(params: Params) {


        val conf = new SparkConf()
            .setAppName("KMeansTest")
            //.set("spark.executor.extraJavaOptions", "-XX:+PrintGC")
            .set("spark.executor.memory", params.heapSize + "g")


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

        val sparseVectorListRDD = sc.parallelize(sparseVectorList, params.numSlices)
        val clusters = KMeans.train(sparseVectorListRDD, params.k, params.numIterations, 1, KMeans.RANDOM)

        //This part becomes reallly slow when number of clusters is large
        // // Evaluate clustering by computing Within Set Sum of Squared Errors
        // val WSSSE = clusters.computeCost(sparseVectorListRDD)
        // println("Within Set Sum of Squared Errors = " + WSSSE)
    }
}
