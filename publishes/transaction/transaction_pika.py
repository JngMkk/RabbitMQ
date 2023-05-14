from pika import (
    PlainCredentials,
    ConnectionParameters,
    BlockingConnection,
    BasicProperties,
)

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
    ROUTING_KEY,
    EXCHANGE,
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
)


CREDENTIALS = PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = ConnectionParameters(host=HOST, port=PORT, credentials=CREDENTIALS)


with BlockingConnection(parameters=PARAMS) as conn:
    channel = conn.channel()

    channel.tx_select()

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body="transaction test message",
        properties=BasicProperties(
            content_type="text/plain", delivery_mode=2, type="transaction"
        ),
    )

    if (resp := channel.tx_commit()) is not None:
        print(resp)
        # * <METHOD(['channel_number=1', 'frame_type=1', 'method=<Tx.CommitOk>'])>
