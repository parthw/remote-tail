"""
Tail Cli to start and stopping remote tail
Usage - python main.py <IP ADDRESS> <FILE PATH>
"""
import os
import sys

import requests
import yaml
from kafka import KafkaConsumer

# Reading kafka-servers and kafka-topic from config-file
dir_path = os.path.dirname(os.path.realpath(__file__))
config = yaml.safe_load(open(os.path.join(dir_path, "config/config.yml")))


def start_agent_process(ipaddr, filepath):
    """
    ipaddr: ip address to start tail process
    filepath: full path of file to tail

    Logic - To start the tail by doing post request
    """
    start_url = f"http://{ipaddr}:5000/start"
    try:
        response = requests.post(url=start_url, json={"filepath": filepath})
    except Exception as expn:
        return False, expn
    print(response.content.decode("utf-8"))
    if response.status_code == 200:
        return True, None
    return False, f"Failed to start {ipaddr} agent tail process"


def stop_agent_process(ipaddr):
    """
    ipaddr: ip address of server to stop tail process

    Logic - To stop tail process on agent server
    """
    stop_url = f"http://{ipaddr}:5000/stop"
    try:
        response = requests.get(url=stop_url)
    except Exception as expn:
        return False, expn
    print(response.content.decode("utf-8"))
    if response.status_code == 200:
        return True, None
    return False, f"Failed to stop {ipaddr} agent tail process"


def start_tailing(ipaddr, filepath):
    """
    ipaddr: ip address of server to tail
    filepath: full path of file to tail

    Logic - Print the tail by subscribing from kafka
    """

    status, expn = start_agent_process(ipaddr, filepath)
    if not status:
        print(expn)
        return

    consumer = KafkaConsumer(
        config["kafka-topic"],
        bootstrap_servers=config["kafka-servers"],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group')

    try:
        for msg in consumer:
            print(msg.value.decode("utf-8"))
    except KeyboardInterrupt:
        status, expn = stop_agent_process(ipaddr)
        if not status:
            print(expn)
        return


if __name__ == '__main__':
    start_tailing(sys.argv[1], sys.argv[2])
