import os
import sys

# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/ozlem/Downloads/spark-2.0.0-bin-hadoop2.4"
#Line above should be adjusted according to local spark folder

try:
    from pyspark.sql import SparkSession
    from pyspark.ml.classification import LogisticRegression
    from pyspark.ml.evaluation import BinaryClassificationEvaluator
    from pyspark.ml.feature import VectorAssembler
    from pyspark.sql.types import *
    from pyspark.sql.functions import udf
    from pyspark.streaming import StreamingContext
    from pyspark.streaming.kafka import KafkaUtils
except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)


'''
To test this code run the Netcat with following command. Then send any text by typing on command line
$nc -lk 9999
'''
spark = SparkSession.builder \
    .master("local[2]") \
    .appName("NetworkCount") \
    .getOrCreate()
# Initialize SparkContext
sc = spark.sparkContext

ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)
# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))
print type(words)
# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate