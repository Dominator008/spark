import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object KMeansTest {

  def main(args: Array[String]) {

	val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)

	// Load and parse the data
	val data = sc.textFile("/Users/yunmingzhang/Documents/Research/spark/data/mllib/kmeans_data.txt")
	val parsedData = data.map(s => Vectors.dense(s.split(' ').map(_.toDouble))).cache()

	// Cluster the data into two classes using KMeans
	val numClusters = 2
	val numIterations = 20
	val clusters = KMeans.train(parsedData, numClusters, numIterations)

	// Evaluate clustering by computing Within Set Sum of Squared Errors
	val WSSSE = clusters.computeCost(parsedData)
	println("Within Set Sum of Squared Errors = " + WSSSE)

	}
}