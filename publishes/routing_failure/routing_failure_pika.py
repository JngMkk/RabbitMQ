from pika import (
    PlainCredentials,
    ConnectionParameters,
    BlockingConnection,
    BasicProperties,
)
from time import time

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from config.config_pika import EXCHANGE, USERNAME, PASSWORD, HOST, PORT

CREDENTIALS = PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = ConnectionParameters(host=HOST, port=PORT, credentials=CREDENTIALS)

body = "routing failure test"
properties = BasicProperties(
    content_type="text/plain", timestamp=int(time()), type="routing failure"
)


def on_return_callback(channel, method, properties, body):
    """
    Call when a message cannot be routed,
    and should be able to see the basic.return values.
    """

    print("Message returned:")
    print(f" - Method: {method}")
    print(f" - Properties: {properties}")
    print(f" - Body: {body.decode()}")


with BlockingConnection(parameters=PARAMS) as conn:
    channel = conn.channel()

    channel.add_on_return_callback(on_return_callback)

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key="routing.failure.test",
        body=body,
        properties=properties,
        mandatory=True,
    )

    # * Allow the server to send back the basic.return frame
    # * Basic.Return을 포함하여 채널에 대해 사용 가능한 모든 이벤트 처리
    # * time_limit: 이벤트 처리에 소요되는 최대 시간을 지정하는 부동 소수점
    # * time_limit=0.5: 최대 0.5초 동안 이벤트를 처리한다는 의미
    conn.process_data_events(time_limit=0.5)

    """
    Message returned:
    - Method: <Basic.Return(['exchange=test.pika', 'reply_code=312', 'reply_text=NO_ROUTE', 'routing_key=routing.failure.test'])>
    - Properties: <BasicProperties(['content_type=text/plain', 'timestamp=1682255068', 'type=routing failure'])>
    - Body: routing failure test
    """
