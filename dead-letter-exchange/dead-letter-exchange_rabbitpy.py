from rabbitpy import Connection, Exchange, Queue

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL  # noqa:E402


with Connection(URL) as conn:
    with conn.channel() as channel:
        Exchange(channel=channel, name="dead-letter-test").declare()
        queue = Queue(
            channel=channel,
            name="dead-letter-queue",
            arguments={"x-dead-letter-exchange": "dead-letter-test"},
        )
        queue.declare()
