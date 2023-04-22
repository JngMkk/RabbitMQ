import rabbitpy

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import (  # noqa:E402
    URL,
    EXCHANGE,
    QUEUE,
    ROUTING_KEY,
)


# * RabbitMQ 연결
with rabbitpy.Connection(URL) as conn:
    # * 커넥션에 새로운 채널 열기
    with conn.channel() as channel:
        # * 채널을 인자로 전달해서 새로운 Exchange 객체 생성
        exchange = rabbitpy.Exchange(channel=channel, name=EXCHANGE)

        # * RabbitMQ 서버에 Exchange 선언하기
        exchange.declare()

        # * 채널을 전달해 새로운 Queue 객체 생성하기
        queue = rabbitpy.Queue(channel=channel, name=QUEUE)

        # * RabbitMQ 서버에 Queue 선언하기
        msg_cnt, consumer_cnt = queue.declare()
        print(msg_cnt, consumer_cnt)  # 0, 0

        # * RabbitMQ 서버의 Queue와 Exchange 연결
        is_binded = queue.bind(source=exchange, routing_key=ROUTING_KEY)
        print(is_binded)  # 성공하면 True

        for msg_num in range(10):
            # * Message 객체
            # * 자동 직렬화 해주네요.. ㅎ
            msg = rabbitpy.Message(
                channel=channel,
                body_value={"msg_num": msg_num, "message": "test message"},
                properties={"content_type": "application/json"},
                opinionated=True,
            )
            # * 발행
            is_published = msg.publish(
                exchange=exchange,
                routing_key=ROUTING_KEY,
            )
            print(is_published)  # None

# * localhost:15672 에서 확인

# ! guest/guest로 로그인 안될 시
# ! rabbitmqctl add_user test test
# ! rabbitmqctl set_user_tags test administrator
# ! rabbitmqctl set_permissions -p / test ".*" ".*" ".*"

# * Neck message requeue true
# * 관리자 UI에 표시하기 위해 RabbitMQ를 소비할 때 메시지를 Queue에 다시 추가하도록 함
