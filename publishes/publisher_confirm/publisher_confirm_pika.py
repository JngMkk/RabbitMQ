from pika import PlainCredentials, ConnectionParameters, BasicProperties
from pika.adapters import SelectConnection
from pika.channel import Channel
from pika.exceptions import ConnectionClosed

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from config.config_pika import (
    EXCHANGE,
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
)

CREDENTIALS = PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = ConnectionParameters(host=HOST, port=PORT, credentials=CREDENTIALS)

body = "publisher confirm test"
properties = BasicProperties(content_type="text/plain", type="test")


def on_ack_nack(method_frame):
    print(f"Message {method_frame}")
    # * Message <METHOD(['channel_number=1', 'frame_type=1', "method=<Basic.Ack(['delivery_tag=1', 'multiple=False'])>"])>


def on_channel_open(channel: Channel):
    channel.confirm_delivery(ack_nack_callback=on_ack_nack)
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key="publisher.confirm.test",
        body=body,
        properties=properties,
    )
    channel.close()


def on_connection_open(connection: SelectConnection):
    connection.channel(on_open_callback=on_channel_open)


def on_connection_closed(
    connection: SelectConnection, closed_exception: ConnectionClosed
):
    print(f"connection closed: {closed_exception}")
    connection.ioloop.call_later(2, connection.ioloop.stop)


connection = SelectConnection(
    parameters=PARAMS,
    on_open_callback=on_connection_open,
    on_close_callback=on_connection_closed,
)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
