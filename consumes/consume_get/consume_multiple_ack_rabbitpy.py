from rabbitpy import Connection, Queue
from typing import Final

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


PREFETCH_COUNT: Final[int] = 10

with Connection(URL) as conn:
    with conn.channel() as channel:
        channel.prefetch_count(PREFETCH_COUNT)

        # * 미확인 메시지
        unacknowledged = 0

        for msg in Queue(channel=channel, name="test-queue"):
            msg.pprint()
            unacknowledged += 1
            if unacknowledged == PREFETCH_COUNT:
                # * 이전의 모든 미확인 메시지를 수신 확인
                msg.ack(all_previous=True)
                unacknowledged = 0
