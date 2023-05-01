from rabbitpy import Connection, Queue

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL  # noqa:E402


with Connection(URL) as conn:
    with conn.channel() as channel:
        # * QoS 메시지 prefetch count를 10으로 설정
        # * no-ack 옵션을 설정하면 Prefetch 크기가 무시됨.
        channel.prefetch_count(10)
        for msg in Queue(channel=channel, name="test-queue"):
            msg.pprint()
            msg.ack()
