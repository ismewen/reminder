import os

import asyncio
import aio_pika

import django
from django.conf import settings


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
        print("on message")
        print("message")
        print(message)
        pass

    async def test_task(self):
        await self.initialize()
        import ipdb
        ipdb.set_trace()
        await self.exchange.publish(
            aio_pika.Message(b"we all love php"),
            self.routing_key,
        )

    def test(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.test_task())