import rabbitpy

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from config.config_rabbitpy import URL, QUEUE


with rabbitpy.Connection(URL) as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel=channel, name=QUEUE)

        while len(queue) > 0:
            # * 메시지 가져오기
            msg: rabbitpy.Message = queue.get()
            print("***** Message *****")
            print(f"  ID: {msg.properties['message_id']}")
            print(f"  Time: {msg.properties['timestamp'].isoformat()}")
            print(f"  Body: {msg.body.decode()}")

            # * RabbitMQ에 메시지 수신 확인을 전송함
            msg.ack()
