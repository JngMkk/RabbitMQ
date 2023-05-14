from rabbitpy import Connection, Queue
import time
from rabbitpy.exceptions import AMQPNotFound

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
        queue = Queue(
            channel=channel,
            name="expiring-test",
            arguments={"x-expires": 1000},  # * 1초
        )
        queue.declare()

        # * 패시브 Queue 선언을 사용해 Queue의 메시지 및 소비자 수 얻기
        messages, consumers = queue.declare(passive=True)
        print(messages, consumers)
        time.sleep(2)

        try:
            messages, consumers = queue.declare(passive=True)
            print(messages, consumers)
        except AMQPNotFound:
            print("The Queue no longer exists")
