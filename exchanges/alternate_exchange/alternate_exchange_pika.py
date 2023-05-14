from pika import (
    PlainCredentials,
    ConnectionParameters,
    BlockingConnection,
    BasicProperties,
)
from pika.exchange_type import ExchangeType

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from config.config_pika import USERNAME, PASSWORD, HOST, PORT


CREDENTIALS = PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = ConnectionParameters(host=HOST, port=PORT, credentials=CREDENTIALS)


with BlockingConnection(parameters=PARAMS) as conn:
    channel = conn.channel()

    alter_exchange = channel.exchange_declare(
        exchange="alter_exchange",
        exchange_type=ExchangeType.fanout,
    )

    exchange = channel.exchange_declare(
        exchange="main_exchange",
        exchange_type=ExchangeType.topic,
        arguments={"alternate-exchange": "alter_exchange"},
    )

    queue = channel.queue_declare(queue="unroutable-messages")
    if channel.queue_bind(
        queue="unroutable-messages", exchange="alter_exchange", routing_key="#"
    ):
        print("Queue bound to alternate-exchange")

    channel.basic_publish(
        exchange="main_exchange",
        routing_key="",
        body="test",
        properties=BasicProperties(content_type="text/plain"),
    )
