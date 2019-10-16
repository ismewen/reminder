import json
import aio_pika
import django.dispatch
from django.dispatch import receiver

pikachu_consumer = django.dispatch.Signal(providing_args=["message"])


@receiver(pikachu_consumer)
def on_message(message: aio_pika.IncomingMessage, **kwargs):
    body = message.body.decode()
    payload = json.loads(body)
    handle_cls = Processor.registry.get(payload.get("type"))
    handle = handle_cls(payload)
    handle.handle()


class Processor(object):
    message_type = None

    registry = dict()

    def __init_subclass__(cls, **kwargs):
        cls.registry[cls.message_type] = cls

    def __init__(self, payload):
        self.payload = payload

    def handle(self):
        pass


class ExceptionProcessor(Processor):
    message_type = "exception"

    def handle(self):
        print("handle exception message")
        pass
