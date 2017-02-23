# KafkaTheTrial
SparkStreamingKafka.py
Can be used to read text sent by a kafka producer for a given topic and then count the words in the text.

To test this code with Kafka kafka_2.11-0.10.1.1 and Spark 2.0.0

1.Download and unzip kafka_2.11-0.10.1.1.

2.add following line to $SPARK_HOME/conf/spark-defaults.conf
spark.jars.packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0

3.Start Zookeeper server
 ~/Downloads/kafka_2.11-0.10.1.1/bin $ ./zookeeper-server-start.sh  ../config/zookeeper.properties
4.Start Kafka server
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-server-start.sh ../config/server.properties
5.Create topic with name "test"
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
6.Start producer
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-console-producer.sh --broker-list localhost:9092 --topic test
7.Start consumer
~/Downloads/kafka_2.11-0.10.1.1/bin $ ./kafka-console-consumer.sh  --zookeeper localhost:2181 --topic test --from-beginning
8.Run SparkStreamingKafka.py
9.Type some text in producer terminal.
10.Monitor output of SparkStreamingKafka.py
