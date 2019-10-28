import json

import requests

from django.conf import settings

class Inform(object):

    transport = None
    registry = dict()

    def __init_subclass__(cls, **kwargs):
        assert cls.transport not in cls.registry
        cls.registry[cls.transport] = cls
        super(Inform, cls).__init_subclass__(**kwargs)

    def inform(self, message):
        pass


class MattermostTransport(Inform):

    transport = "mattermost"

    def __init__(self, payload):
        self.payload = payload

    @property
    def webhook(self):
        return settings.MATTERMOST_WEBHOOKS_MAPPING.get(self.payload.get("type"))

    def inform(self, content):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "text": content
        }

        res = requests.post(self.webhook, data=json.dumps(data), headers=headers)




class WeChatTransport(Inform):

    transport = "weixin"

    def inform(self, content):
        pass
