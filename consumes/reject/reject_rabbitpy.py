from rabbitpy import consume

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from config.config_rabbitpy import URL, QUEUE


for msg in consume(URL, QUEUE):
    msg.pprint()
    print(f"Redelivered: {msg.redelivered}")

    # * Reject requeue
    msg.reject(requeue=True)
