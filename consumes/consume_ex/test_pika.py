from pika import PlainCredentials, ConnectionParameters, BlockingConnection
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from config.config_pika import QUEUE, USERNAME, PASSWORD, HOST, PORT

CREDENTIALS = PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = ConnectionParameters(host=HOST, port=PORT, credentials=CREDENTIALS)

with BlockingConnection(parameters=PARAMS) as conn:
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
