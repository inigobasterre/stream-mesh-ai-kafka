import json
import logging
import os
from pprint import pformat
import sys
from fetch_youtube_api import fetch_playlist_items, fetch_videos
from utils import summarise_video
from kafka import KafkaProducer
from kafka.errors import KafkaError


def main():
    logging.info("START")
    API_KEY = os.environ.get("API_KEY")
    PLAYLIST_ID = os.environ.get("PLAYLIST_ID")

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda m: json.dumps(m).encode('ascii'))

    
    for video_item in fetch_playlist_items(API_KEY, PLAYLIST_ID):
        for video in fetch_videos(API_KEY, video_item.get('contentDetails').get('videoId')):
            logging.info("GOT %s", pformat(summarise_video(video)))
            producer.send(topic="youtube-videos",value=summarise_video(video))




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
