import pika
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_pika import (  # noqa:E402
    QUEUE,
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
)


CREDENTIALS = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = pika.ConnectionParameters(
    host=HOST, port=PORT, credentials=CREDENTIALS
)

with pika.BlockingConnection(parameters=PARAMS) as conn:
    channel = conn.channel()

    while True:
        method, properties, body = channel.basic_get(
            queue=QUEUE, auto_ack=True
        )

        if method is None:
            break

        else:
            # * pika는 message_id, timestamp 등을 자동으로 만들어주지 않음.
            print("***** Message *****")
            print(f"  Method: {method}")
            print(f"  ID: {properties.message_id}")
            print(f"  Time: {properties.timestamp}")
            print(f"  Body: {body.decode()}")
