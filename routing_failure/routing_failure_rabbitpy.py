from datetime import datetime
from rabbitpy import Connection, Message
from rabbitpy.exceptions import MessageReturnedException

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL, EXCHANGE  # noqa:E402

body = "routing failure test"
properties = {
    "content_type": "text/plain",
    "timestamp": datetime.now(),
    "message_type": "routing failure",
}

with Connection(URL) as conn:
    try:
        with conn.channel() as channel:
            msg = Message(
                channel=channel, body_value=body, properties=properties
            )

            # * Exchange와 Routing Key에 바인딩한 Queue가 없기 때문에 라우팅할 수 없음
            # * Exception은 Channel 수준에서 난다!!
            is_published = msg.publish(
                exchange=EXCHANGE,
                routing_key="routing.failure.test",
                mandatory=True,
            )
            print(is_published)  # None
    except MessageReturnedException as e:
        print(f"Publish failed: {e}")
        # * Message was returned by RabbitMQ: (312) for exchange NO_ROUTE


"""
rabbitpy 라이브러리에서 클라이언트는 Basic.Return을 자동으로 수신하며,
채널 범위에서 수신하면 MessageReturnedException을 발생시킴.

다른 라이브러리의 경우,
메시지를 발행할 때 RabbitMQ에서 Basic.Return RPC를 전달받으면 실행할 콜백 메소드를 등록해야 할 수도 있음.
비동기적으로 Basic.Return 메시지를 처리할 때 다른 메시지를 소비하는 것처럼
Basic.Return 메소드 프레임, 콘텐츠 헤더 프레임, 바디 프레임을 받게 됨.
"""
