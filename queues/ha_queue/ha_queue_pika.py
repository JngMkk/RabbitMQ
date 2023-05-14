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

from config.config_pika import USERNAME, PASSWORD, HOST, PORT


CREDENTIALS = PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = ConnectionParameters(host=HOST, port=PORT, credentials=CREDENTIALS)


with BlockingConnection(parameters=PARAMS) as conn:
    channel = conn.channel()

    queue = channel.queue_declare(
        queue="HA-Queue", arguments={"x-ha-policy": "all"}
    )

    queue2 = channel.queue_declare(
        queue="HA-Queue2",
        arguments={
            "x-ha-policy": "nodes",
            "x-ha-nodes": ["rabbit@node1", "rabbit@node2"],
        },
    )

    if queue:
        print(queue)

    if queue2:
        print(queue2)
