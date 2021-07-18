"""
Tailer.py file to read the content of file and
push them to kafka server
"""

import logging
import os

import yaml
from kafka import KafkaProducer

# Reading configuration file
dir_path = os.path.dirname(os.path.realpath(__file__))
config = yaml.safe_load(open(os.path.join(dir_path, "config/config.yml")))

# Connecting to Kafka
producer = KafkaProducer(bootstrap_servers=config["kafka-servers"])

# Setting up logging
logging.getLogger().setLevel(logging.INFO)


def tail(filepath):
    """
    filepath: input filepath to read the content
    Logic to tail the provided filepath
    """
    if os.path.isfile(filepath):
        logging.info("Starting to tail %s", filepath)
        file_object = open(filepath)
        file_pointer = 0

        # Setting the file pointer at the end of file
        file_object.seek(file_pointer, os.SEEK_END)

        while True:
            content = file_object.readline()
            if not send_to_server(content):
                break
            file_pointer = file_object.tell()

            # Handling file truncate situation
            # This is for log-rotate scenarios
            file_size = os.stat(file_object.fileno()).st_size
            if file_size < file_pointer:
                file_pointer = 0

            file_object.seek(file_pointer)

    else:
        logging.error("File %s does not exist", filepath)
        return f"File {filepath} does not exist"


def send_to_server(content):
    """
    content: tail content
    Logic to push the tail content to pusher server
    """
    try:
        if content:
            producer.send(config["kafka-topic"], value=bytes(content, 'utf-8'))
            # producer.flush()
    except Exception as expn:
        logging.error(
            "Exception occured while sending content to server - %s", expn)
        return False
    return True
