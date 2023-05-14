import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from rabbitpy import Queue, Connection, Message
from config.config_rabbitpy import URL
import time
from exchanges import utils


conn = Connection(URL)
channel = conn.channel()

queue_name = f"response-queue-{os.getpid()}"
response_queue = Queue(
    channel=channel, name=queue_name, exclusive=True, auto_delete=False
)

if response_queue.declare():
    print("Response queue declared.")

if response_queue.bind("rpc-replies", queue_name):
    print("Response queue bound.")

for img_id, filename in enumerate(utils.get_images()):
    print(f"Sending request for image {img_id}: {filename}")

    message = Message(
        channel=channel,
        body_value=utils.read_image(filename),
        properties={
            "content_type": utils.mime_type(filename),
            "correlation_id": str(img_id),
            "reply_to": queue_name,
        },
        opinionated=True,
    )

    message.publish(exchange="direct-rpc-requests", routing_key="detect-faces")

    message = None
    while not message:
        time.sleep(0.5)
        message = response_queue.get()

    message.ack()

    duration = time.time() - time.mktime(
        message.properties["headers"]["first_publish"]
    )

    print(
        f"""
        Facial detection RPC call for image...
        {message.properties['correlation_id']} total duration: {duration}
        """
    )

print("RPC requests processed.")
channel.close()
conn.close()
