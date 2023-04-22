import pika
import json

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_pika import (  # noqa:E402
    QUEUE,
    EXCHANGE,
    ROUTING_KEY,
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
)

CREDENTIALS = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
PARAMS = pika.ConnectionParameters(
    host=HOST, port=PORT, credentials=CREDENTIALS
)

# * RabbitMQ 연결
with pika.BlockingConnection(parameters=PARAMS) as conn:
    # * 커넥션에 새로운 채널 열기
    channel = conn.channel()

    # * Exchange 선언
    exchange_resp = channel.exchange_declare(
        exchange=EXCHANGE, exchange_type="direct"
    )
    print(exchange_resp)
    # * response: channel_number, frame_type, Exchange.DeclareOk

    # * Queue 선언
    queue_resp = channel.queue_declare(QUEUE)
    print(queue_resp)
    # * response: channel_number, frame_type, Queue.DeclareOk
    # * Queue.DeclareOk response: [consumer_count, message_count, queue]

    # * Queue와 Exchange 연결
    bind_resp = channel.queue_bind(
        queue=QUEUE,
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
    )
    print(bind_resp)
    # * response: channel_number, frame_type, Queue.BindOk

    for msg_num in range(10):
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=ROUTING_KEY,
            body=json.dumps({"msg_num": msg_num, "msg": "test message"}),
            properties=pika.BasicProperties(content_type="application/json"),
        )
