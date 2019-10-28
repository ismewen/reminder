import os

import asyncio
import traceback

import aio_pika
import json

import django
from django.conf import settings

from modules.worker.handle import pikachu_consumer


class PikaChu(object):
    connection: aio_pika.Connection
    exchange_name: str
    exchange: aio_pika.Exchange
    routing_key = "exception"
    channel: aio_pika.Channel
    queue: aio_pika.RobustQueue

    async def initialize(self):
        # create connection
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.connection = connection

        channel = await connection.channel()
        self.channel = channel
        # declare exchange
        exchange = await channel.declare_exchange(
            "jcy", aio_pika.ExchangeType.DIRECT, durable=True,
        )
        self.exchange = exchange
        # declare queue
        queue = await channel.declare_queue(durable=True)

        self.queue = queue
        # bind exchange
        await queue.bind(self.exchange, self.routing_key)

    async def _consumer(self):
        await self.initialize()
        async with self.connection:
            async with self.queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        self.on_message(message)

    def consumer(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._consumer())
        loop.run_forever()

    def on_message(self, message: aio_pika.IncomingMessage):
        try:
            pikachu_consumer.send(sender=self, message=message)
        except Exception as e:
            print("traceback:")
            print(traceback.format_exc())
            print("consumer failed")

    async def _publish(self, payload):
        await self.initialize()
        await self.exchange.publish(
            aio_pika.Message(payload),
            self.routing_key,
        )

    def publish(self, payload):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        payload = payload.encode()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._publish(payload))

    def test(self):
        payload = {
            "type": "ticket",
            "msg": "we all love php"
        }
        self.publish(payload=payload)
