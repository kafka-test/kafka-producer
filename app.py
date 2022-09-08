#!/usr/bin/env python

import os
from kafka import KafkaProducer
import json
from bson import json_util
import time
    
def send_message(counter, topic):
    message = {'value': counter}
    producer.send(topic, json.dumps(message, default = json_util.default).encode('utf-8'))

# 'kafka-cluster-kafka-rtlistener-bootstrap-openshift-operators.apps-crc.testing:443'
kafka_server = os.environ['KAFKA_SERVER']
kafka_topic_1 = os.environ['KAFKA_TOPIC_1']
kafka_topic_2 = os.environ['KAFKA_TOPIC_2']

print("Producing messages to Kafka topic ...")
producer = KafkaProducer(bootstrap_servers = kafka_server,
                         ssl_cafile = '/mnt/kafka-config/ca.crt',
                         security_protocol="SSL")

i = 0
while True:
    i += 1
    topic = kafka_topic_1 if (i % 2) == 1 else kafka_topic_2
    send_message(i, topic)
    time.sleep(0.5)
  