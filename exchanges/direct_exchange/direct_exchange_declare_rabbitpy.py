import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        )
    )
)

from rabbitpy import Connection, DirectExchange
from config.config_rabbitpy import URL


with Connection(URL) as conn:
    with conn.channel() as channel:
        for _exchange in ("rpc-replies", "direct-rpc-requests"):
            exchange = DirectExchange(channel=channel, name=_exchange)
            exchange.declare()
