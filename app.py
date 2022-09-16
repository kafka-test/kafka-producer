#!/usr/bin/env python

import os
from kafka import KafkaProducer, KafkaAdminClient, NewTopic, UnknownTopicOrPartitionError, TopicAlreadyExistsError
from json import dumps
from kafka.admin.new_partitions import NewPartitions
from time import sleep

consumer = KafkaConsumer(bootstrap_servers = kafka_server,
                         ssl_cafile = '/mnt/kafka-config/ca.crt',
                         security_protocol="SSL")

def create_topics(topic_names):
    existing_topic_list = consumer.topics()
    print(list(consumer.topics()))
    topic_list = []
    for topic in topic_names:
        if topic not in existing_topic_list:
            print('Topic : {} added '.format(topic))
            topic_list.append(NewTopic(name=topic, num_partitions=12, replication_factor=3))
        else:
            print('Topic : {topic} already exist ')
    try:
        if topic_list:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print("Topic Created Successfully")
        else:
            print("Topic Exist")
    except TopicAlreadyExistsError as e:
        print("Topic Already Exist")
    except  Exception as e:
        print(e)

# 'dev-kafka-cluster-kafka-ext-bootstrap-openshift-operators.apps-crc.testing:443'
# 'stg-kafka-cluster-kafka-ext-bootstrap-openshift-operators.apps-crc.testing:443'
hostname = os.environ['HOSTNAME']
kafka_server = os.environ['KAFKA_SERVER']
kafka_topic_1 = os.environ['KAFKA_TOPIC_1']
kafka_topic_2 = os.environ['KAFKA_TOPIC_2']

admin_client = KafkaAdminClient(bootstrap_servers = kafka_server,
                                ssl_cafile = '/mnt/kafka-config/ca.crt',
                                security_protocol="SSL")

topic_names = [kafka_topic_1, kafka_topic_2]
try:
    admin_client.delete_topics(topics=topic_names)
    print("Topic Deleted Successfully")
except UnknownTopicOrPartitionError as e:
    print("Topic Doesn't Exist")
    print(e)
except  Exception as e:
    print(e)
    
create_topics(topic_names)

try:
    admin_client.create_partitions({
        kafka_topic_1: NewPartitions(10),
        kafka_topic_2: NewPartitions(10)
    })
except:
    err_msg = "Topics {} {} already have partitions".format(kafka_topic_1, kafka_topic_2)
    print(err_msg)

print("Producing messages to Kafka topic ...")
producer = KafkaProducer(bootstrap_servers = kafka_server,
                         ssl_cafile = '/mnt/kafka-config/ca.crt',
                         security_protocol="SSL",
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

i = 0
while True:
    i += 1
    msg = hostname + ' ' + str(i)
    topic = kafka_topic_1 if (i % 2) == 1 else kafka_topic_2
    producer.send(topic, value = msg)
    sleep(0.5)
    
  