import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

import time
from exchanges import detect, utils

from rabbitpy import Connection, Queue, Message
from config.config_rabbitpy import URL


conn = Connection(URL)
channel = conn.channel()

# * Queue를 일시적으로 생성
# * 소비자 애플리케이션의 한 인스턴스에서만 사용할 수 있도록 함.
# * 소비자 애플리케이션이 중지되면 즉시 큐를 제거하도록 auto_delete = True / durable = False
# * 다른 애플리케이션이 큐의 메시지에 접근할 수 없도록 exclusive = True
# * 다른 애플리케이션이 접근하려고 하면 Channel.Close 프레임 전송
queue_name = f"rpc-worker-{os.getpid()}"
queue = Queue(
    channel=channel, name=queue_name, exclusive=True, auto_delete=True
)

if queue.declare():
    print("Worker queue declared.")

if queue.bind(source="direct-rpc-requests", routing_key="detect-faces"):
    print("Worker queue bound.")


for message in queue.consume_messages():
    duration = time.time() - int(
        message.properties["timestamp"].strftime("%s")
    )
    print(f"Received RPC request published {duration:.2f} seconds ago")

    temp_file = utils.write_temp_file(
        message.body, message.properties["content_type"]
    )

    result_file = detect.faces(temp_file)

    properties = {
        "app_id": "Detecting Face Worker",
        "content_type": message.properties["content_type"],
        "correlation_id": message.properties["correlation_id"],
        "headers": {"first_publish": message.properties["timestamp"]},
    }

    body = utils.read_image(result_file)

    os.unlink(temp_file)

    os.unlink(result_file)

    response = Message(
        channel=channel,
        body_value=body,
        properties=properties,
        opinionated=True,
    )
    response.publish(
        exchange="rpc-replies", routing_key=message.properties["reply_to"]
    )
    message.ack()
