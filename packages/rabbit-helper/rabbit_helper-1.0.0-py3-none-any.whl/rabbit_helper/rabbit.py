import json
import logging
import math
import time

import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel

logging.basicConfig(level=logging.INFO)


class Rabbit:
    def __init__(self, rabbit_url):
        self.rabbit_url = rabbit_url
        self._connection: BlockingConnection = None
        self._channel: BlockingChannel = None

    async def _connect(self):
        counts = 0

        while True:
            try:
                connection = pika.BlockingConnection(pika.URLParameters(self.rabbit_url))
                channel = connection.channel()
                logging.info("Connected to the rabbitMQ")
                break
            except Exception as e:
                logging.warning("rabbitmq not yet ready...")
                counts += 1

                if counts > 5:
                    logging.error(f"Failed to connect to RabbitMQ: {e}")
                    return

                back_off = math.pow(counts, 2)
                logging.info(f"Backing off for {back_off} seconds")

                time.sleep(back_off)

        self._connection = connection
        self._channel = channel

    async def publish(self, routing_key, data) -> bool:
        if not self._connection or not self._channel:
            await self._connect()

        try:
            self._queue_declare(routing_key)

            json_data = json.dumps(data)
            self._channel.basic_publish(exchange="", routing_key=routing_key, body=json_data,
                                        properties=pika.BasicProperties(content_type="application/json"))
            logging.info(f"published message: {data} to queue: {routing_key}")
            return True
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")
            return False

    async def consume(self, routing_key, callback):
        if not self._channel or not self._connection:
            await self._connect()
        while True:
            try:
                self._queue_declare(routing_key)

                self._channel.basic_consume(queue=routing_key, on_message_callback=callback, auto_ack=True)
                logging.info(f"Started consuming from queue: {routing_key}")
                self._channel.start_consuming()

            except Exception as e:
                logging.error(f"Failed to consume message: {e}")

    def _queue_declare(self, routing_key):
        self._channel.queue_declare(queue=routing_key)

    def close(self):
        if self._channel:
            self._channel.close()
        if self._connection:
            self._connection.close()
