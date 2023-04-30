from rabbitpy import Connection, Tx, Message
from rabbitpy.exceptions import NoActiveTransactionError

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL, EXCHANGE, ROUTING_KEY  # noqa:E402


with Connection(URL) as conn:
    with conn.channel() as channel:
        # * 트랜잭션 객체 생성
        tx = Tx(channel=channel)

        # * 트랜잭션 시작
        tx.select()

        msg = Message(
            channel=channel,
            body_value="transaction test message",
            properties={
                "content_type": "text/plain",
                "delivery_mode": 2,
                "message_type": "transaction",
            },
        )

        msg.publish(exchange=EXCHANGE, routing_key=ROUTING_KEY)

        try:
            if tx.commit():
                print("Transaction committed")
        except NoActiveTransactionError:
            print("Tried to commit without active transaction")
