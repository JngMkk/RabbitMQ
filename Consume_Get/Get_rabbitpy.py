from rabbitpy import Connection, Queue

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL  # noqa:E402


with Connection(URL) as conn:
    with conn.channel() as channel:
        queue = Queue(channel=channel, name="test-queue")

        while True:
            msg = queue.get()
            if msg:
                msg.pprint()
                # * Exchange:
                # * Routing Key: test-queue
                # * bytearray(b'go')
                msg.ack()
                if msg.body.decode() == "stop":
                    break
