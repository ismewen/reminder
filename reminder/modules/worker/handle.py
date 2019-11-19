import json
import aio_pika
import django.dispatch
from django.dispatch import receiver

from modules.apps.exceptionlog.models import ExceptionRecord
from .inform import Inform

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

    transports = None

    registry = dict()

    def __init_subclass__(cls, **kwargs):
        cls.registry[cls.message_type] = cls

    def __init__(self, payload):
        self.payload = payload

    def handle(self):
        pass

    def inform(self, content):
        transports = [Inform.registry.get(cls_name) for cls_name in self.transports]
        for transport in transports:
            transport(self.payload).inform(content=content)


class ExceptionProcessor(Processor):
    message_type = "exception"

    transports = "mattermost",

    def handle(self):
        print("handle exception message")
        kwargs = {
            "url": self.payload.get("url"),
            "msg": self.payload.get("msg"),
            "traceback": self.payload.get("traceback_info")
        }
        if msg == "watch function has exception":
            continue
        record = ExceptionRecord(**kwargs)
        record.save()
        content = record.build_content()
        print("start to inform")
        self.inform(content=content)


class TicketProcessor(Processor):
    transports = 'mattermost',

    message_type = "ticket"

    def handle(self):
        content = self.payload.get("msg")
        self.inform(content=content)