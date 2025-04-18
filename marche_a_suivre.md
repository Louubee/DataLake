# 3 terminaux ubuntu : 
## Le premier : 
Lance zookeper puis un topic kafka 

sudo /usr/share/zookeeper/bin/zkServer.sh start
sudo /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties

Créer trois topic topic :
sudo /usr/local/kafka/bin/kafka-topics.sh --create --topic social_media --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
sudo /usr/local/kafka/bin/kafka-topics.sh --create --topic text_topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

sudo /usr/local/kafka/bin/kafka-topics.sh --create --topic sqlite_topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1


Le deuxième :
Lance le producer.py
Python3 producer.py

Le troisième :
Lance le consumer.py
Python3 consumer.py



Lancer un script PySpark avec :
Python3 Spark.py



# Annexe :
## list des topics existant :
sudo /usr/local/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

## Supprimer des topics :
sudo /usr/local/kafka/bin/kafka-topics.sh --delete --topic txt_topic  --bootstrap-server localhost:9092

 
