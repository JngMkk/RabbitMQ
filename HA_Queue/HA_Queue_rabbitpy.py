from rabbitpy import Connection, Queue

from rabbitpy.exceptions import RemoteClosedChannelException

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL  # noqa:E402


with Connection(URL) as conn:
    try:
        with conn.channel() as channel:
            queue = Queue(
                channel=channel,
                name="HA-Queue",
                # * HA 정책 모든 서버 노드에 복사
                arguments={"x-ha-policy": "all"},
            )

            if queue.declare():
                print("Queue declared")

    except RemoteClosedChannelException as err:
        print(f"Queue declare failed: {err}")


with Connection(URL) as conn:
    try:
        with conn.channel() as channel:
            queue = Queue(
                channel=channel,
                name="HA-Queue2",
                # * 노드 지정
                arguments={
                    "x-ha-policy": "nodes",
                    "x-ha-nodes": [
                        "rabbit@node1",
                        "rabbit@node2",
                        "rabbit@node3",
                    ],
                },
            )

            if queue.declare():
                print("Queue declared")

    except RemoteClosedChannelException as err:
        print(f"Queue declare failed: {err}")
