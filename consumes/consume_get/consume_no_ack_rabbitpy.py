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
        queue = Queue(channel=channel, name="test-queue")

        # * no_ack=True로 Basic.Consume RPC 요청 전송
        # * 소비자에게 메시지를 전달하는 가장 빠른 방법
        for msg in queue.consume_messages(no_ack=True):
            msg.pprint()
