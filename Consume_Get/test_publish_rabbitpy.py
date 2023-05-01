from rabbitpy import publish

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config.config_rabbitpy import URL  # noqa:E402


for _ in range(10):
    publish(uri=URL, exchange_name="", routing_key="test-queue", body="go")

publish(uri=URL, exchange_name="", routing_key="test-queue", body="stop")
