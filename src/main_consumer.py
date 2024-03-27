import json
import logging
import os
from pprint import pformat
from utils import summarise_video
import sys
from kafka import KafkaConsumer
from kafka.errors import KafkaError


def main():
    logging.info("START")

    consumer = KafkaConsumer("youtube-videos",bootstrap_servers=['localhost:9092'],value_deserializer=lambda m: json.loads(m.decode('ascii')))

    for message in consumer:
            logging.info("GOT %s", pformat(message.value))



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())

    # # Asynchronous by default
    # future = producer.send('my-topic', b'raw_bytes')

    # # Block for 'synchronous' sends
    # try:
    #     record_metadata = future.get(timeout=10)
    # except KafkaError:
    #     # Decide what to do if produce request failed...
    #     log.exception()
    #     pass

    # # Successful result returns assigned partition and offset
    # print (record_metadata.topic)
    # print (record_metadata.partition)
    # print (record_metadata.offset)

    # # produce keyed messages to enable hashed partitioning
    # producer.send('my-topic', key=b'foo', value=b'bar')

    # # produce json messages
    # producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
    # producer.send('json-topic', {'key': 'value'})

    # # handle exception
    # # configure multiple retries
    # producer = KafkaProducer(retries=5)
