import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

from pika import BasicProperties, BlockingConnection, URLParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.adapters.utils.connection_workflow import AMQPConnectorException
from pika.exceptions import (
    AMQPChannelError,
    AMQPConnectionError,
    ChannelClosedByBroker,
    StreamLostError,
)
from pika.exchange_type import ExchangeType
from pika.frame import Method
from pika.spec import Exchange


class StrEnum(str, Enum):
    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=False)
class Message:
    title: str = ""
    body: str
    contents: dict
    send_date: str = field(
        default_factory=lambda: datetime.now()
        .replace(tzinfo=timezone(offset=timedelta(seconds=32400)))
        .isoformat()
    )


class RoutingKeyType(StrEnum):
    NOTICE = "NOTICE"
    REGISTER = "REGISTER"


CONNECTION_ERRORS = (
    AMQPConnectionError,
    AMQPConnectorException,
    AMQPChannelError,
    ChannelClosedByBroker,
    StreamLostError,
)
DEFAULT_CONTENT_TYPE: str = "application/json"
DEFAULT_EXPIRATION: str = "604800000"  # * 1주일
TOPIC_EXCHANGE: str = "amq.topic"


class RabbitBase:
    def __init__(
        self,
        url: str,
        content_type: str = DEFAULT_CONTENT_TYPE,
        expriation: str = DEFAULT_EXPIRATION,
        **kwargs: Any,
    ) -> None:
        params = URLParameters(url=url)
        self._connection_retries = kwargs.get("connection_retries", 3)
        self._connection = self.__connect(params)
        self._channel = self.__channel()
        self._properties = BasicProperties(content_type=content_type, expiration=expriation)

    def __logging_reconnect(self, error: Exception, reties: int) -> None:
        message = f"RabbitMQ tried to reconnect {reties} times.\n{repr(error)}"
        logging.error(message)
        return

    def __connect(self, params: URLParameters, retries: int = 1) -> BlockingConnection:
        try:
            conn = BlockingConnection(params)
        except CONNECTION_ERRORS as err:
            if not retries == self._connection_retries:
                self.__logging_reconnect(err, retries)
                raise err
            time.sleep(2)
            return self.__connect(retries + 1)
        return conn

    def close(self) -> None:
        self._connection.close()
        return

    def __channel(self) -> BlockingChannel:
        try:
            chan = self._connection.channel()
        except CONNECTION_ERRORS as err:
            logging.error(err)
            self.close()
            raise err

        return chan

    def _setup_exchange(
        self,
        exchange_name: str,
        exchange_type: ExchangeType,
        durable: bool,
    ) -> None:
        resp: Method = self._channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type, durable=durable
        )
        if isinstance(resp.method, Exchange.DeclareOk):
            logging.info("Exchange Declared.")
            return

        # TODO: 어떤 Exception 띄울 것인지
        self.close()
        raise Exception


class RabbitHelper(RabbitBase):
    def init_exchange(self) -> None:
        self._setup_exchange(TOPIC_EXCHANGE, ExchangeType.topic, durable=True)
        self.close()
        return

    def __publish(self, exchange: str, routing_key: str, payload: Message) -> None:
        body = json.dumps(payload)
        try:
            self._channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body,
                properties=self._properties,
            )
        except Exception as e:
            logging.error(e)
            self.close()
            raise e
        return

    def publish(
        self, exchange: str, key_type: RoutingKeyType, messages: list[tuple[str, dict[str, Any]]]
    ) -> None:
        for message in messages:
            route_key, msg = message
            if route_key:
                routing_key_prefix = f"agent.{route_key}"
                self.__publish(exchange, f"{routing_key_prefix}.{key_type.lower()}", msg)

        self.close()
