import os
import sys

# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/ozlem/Downloads/spark-2.0.0-bin-hadoop2.4"
#Line above should be adjusted according to local spark folder

try:
    from pyspark.sql import SparkSession
    from pyspark.streaming import StreamingContext
    from pyspark.streaming.kafka import KafkaUtils
except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)



spark = SparkSession.builder \
    .master("local[2]") \
    .appName("KafkaWordCount") \
    .getOrCreate()
# Initialize SparkContext
sc = spark.sparkContext

ssc = StreamingContext(sc, 5)
'''
To test this code add following line to $SPARK_HOME/conf/spark-defaults.conf,start producer, start consumer
spark.jars.packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0
'''
'''
To test this code run following commands(Start zookeeper, start kafka, create topic, start consumer)
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./zookeeper-server-start.sh  ../config/zookeeper.properties
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-server-start.sh ../config/server.properties
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-console-producer.sh --broker-list localhost:9092 --topic test
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-console-consumer.sh  --zookeeper localhost:2181 --topic test --from-beginning

'''

kafkaStream = KafkaUtils.createStream(ssc, "localhost:2181", "test", {"test": 1})
lines = kafkaStream.map(lambda x: x[1])
counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: (a+b))
counts.pprint()

ssc.start()
ssc.awaitTermination()
