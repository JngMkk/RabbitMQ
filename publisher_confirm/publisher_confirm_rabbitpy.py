from rabbitpy import Connection, Message, Channel

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL, EXCHANGE  # noqa:E402

body = "publisher confirm test"
properties = {"content_type": "text/plain", "message_type": "test"}

with Connection(URL) as conn:
    channel: Channel = conn.channel()

    # * 발행자 확인 기능 on
    channel.enable_publisher_confirms()

    msg = Message(channel=channel, body_value=body, properties=properties)

    # * mandatory True로 설정하지 않았기 때문에 에러는 나지 않음
    if msg.publish(exchange=EXCHANGE, routing_key="publisher.confirm.test"):
        print("The message was confirmed")

    channel.close()


"""
rabbitpy에서는 발행자 확인을 사용하기가 매우 쉬움.
보통 다른 라이브러리에서는 Basic.Ack 또는 Basic.Nack 요청에 비동기적으로 응답하는 콜백 핸들러를 전달해야 하지만,
rabbitpy는 구현하기는 쉬우나 확인을 받을 때까지 블로킹되므로 느림.

발행자 확인의 사용 여부와 상관없이 존재하지 않는 Exchange에 메시지를 발행할 경우, 채널은 RabbitMQ에 의해 종료됨.
이 경우 rabbitpy에서는 RemoteClosedChannelException 예외가 발생함.
"""
