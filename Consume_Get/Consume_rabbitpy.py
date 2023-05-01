from rabbitpy import Connection, Queue

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL  # noqa:E402


with Connection(URL) as conn:
    with conn.channel() as channel:
        # for msg in consume(uri=URL, queue_name="get-test-queue"):
        for msg in Queue(channel=channel, name="test-queue"):
            msg.pprint()
            # * Exchange:
            # * Routing Key: test-queue
            # * bytearray(b'go')
            msg.ack()

            if msg.body.decode() == "stop":
                break


"""
반복문이 종료될 때 rabbitpy 라이브러리는 RabbitMQ에 Basic.Cancel 명령을 전송함.
이후 Basic.CancelOk RPC 응답이 수신되면 RabbitMQ가 클라이언트에 처리되지 않는 메시지를 보낸 경우
rabbitpy는 Basic.Nack 명령을 전송하고 RabbitMQ가 메시지를 다시 Queue에 삽입하도록 지시함.
"""
