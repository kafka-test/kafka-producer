#!/usr/bin/env python

import os
from kafka import KafkaProducer, KafkaAdminClient
from json import dumps
from kafka.admin.new_partitions import NewPartitions
from time import sleep

# 'dev-kafka-cluster-kafka-ext-bootstrap-openshift-operators.apps-crc.testing:443'
# 'stg-kafka-cluster-kafka-ext-bootstrap-openshift-operators.apps-crc.testing:443'
hostname = os.environ['HOSTNAME']
kafka_server = os.environ['KAFKA_SERVER']
kafka_topic_1 = os.environ['KAFKA_TOPIC_1']
kafka_topic_2 = os.environ['KAFKA_TOPIC_2']

client = KafkaAdminClient(bootstrap_servers = kafka_server,
                         ssl_cafile = '/mnt/kafka-config/ca.crt',
                         security_protocol="SSL")

try:  
    client.delete_topics([kafka_topic_1, kafka_topic_2])
except:
    err_msg  = "Unable to delete {} or {}".format(kafka_topic_1, kafka_topic_2)
    print(err_msg)

client.create_topics([kafka_topic_1, kafka_topic_2])
rsp = client.create_partitions({
    kafka_topic_1: NewPartitions(10),
    kafka_topic_2: NewPartitions(10)
})

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
  