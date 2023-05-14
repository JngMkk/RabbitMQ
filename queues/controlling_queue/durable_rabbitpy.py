from rabbitpy import Connection, Queue

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from config.config_rabbitpy import URL


with Connection(URL) as conn:
    with conn.channel() as channel:
        queue = Queue(channel=channel, name="durable-test", durable=True)

        if queue.declare():
            print("Queue declared")
