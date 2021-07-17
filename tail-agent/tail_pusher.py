import logging
import os

import pusher

# Configuring pusher client to send files content
pusher_client = pusher.Pusher(
    app_id='1236771',
    key='4658bc9d345bd31db4a8',
    secret='c0d0cbeafdc885eee4e9',
    cluster='ap2',
    ssl=True
)

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
            if not send_to_pusher_server(content):
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


def send_to_pusher_server(content):
    """
    content: tail content
    Logic to push the tail content to pusher server
    """
    try:
        if content:
            print(content)
            # pusher_client.trigger(
            #    'my-channel', 'my-event', {'message': content})
    except Exception as expn:
        logging.error(
            "Exception occured while sending content to pusher server - %s", content)
        return False
    return True
