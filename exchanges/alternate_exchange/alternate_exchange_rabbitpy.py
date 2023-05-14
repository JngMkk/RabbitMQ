from rabbitpy import Connection, Exchange, Queue, Message

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
        # * 대체 Exchange 객체 생성
        alter_exchange = Exchange(
            channel=channel, name="alter_exchange", exchange_type="fanout"
        )
        # * 대체 Exchange 선언
        alter_exchange.declare()

        exchange = Exchange(
            channel=channel,
            name="main_exchange",
            exchange_type="topic",
            arguments={"alternate-exchange": alter_exchange.name},
        )

        exchange.declare()

        # * 라우팅될 수 없는 메시지는 아래 Queue에 저장됨.
        queue = Queue(channel=channel, name="unroutable-messages")
        queue.declare()

        if queue.bind(alter_exchange, "#"):
            print("Queue bound to alternate-exchange")

        msg = Message(
            channel=channel,
            body_value="test",
            properties={"content_type": "text/plain"},
        )
        msg.publish(exchange=exchange)
        # * Queue bound to alternate-exchange


"""
Fanout: 자신이 알고 있는 모든 Queue에 메시지를 전달함.

Topic: 라우팅 키를 기반으로 선택적으로 메시지를 라우팅할 수 있음.
"""
