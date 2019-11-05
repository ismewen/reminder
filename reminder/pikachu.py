import argparse

import os
import traceback

import django

from common.core import discovery


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder.settings')
    django.setup()
    parser = argparse.ArgumentParser(description='Go ahead, PikaChu')
    discovery.discover_views()
    discovery.discovery_signal()
    from common.kaka.pikachu import PikaChu
    from django.conf import settings
    parser.add_argument('pikachu', help='Go ahead, Pikachu', choices=["run", "test"])
    arguments = parser.parse_args()
    print(" **** start init pikachu ***")
    print("settings RABBITMQ_URL %s" % settings.RABBITMQ_URL)
    pikachu = PikaChu()
    print(" *** init down ***")
    action = arguments.pikachu
    if action == "run":
        try:
           pikachu.consumer()
        except KeyboardInterrupt:
            print("existing")
            print(traceback.format_exc())
            exit(0)
    elif action == "test":
        pikachu.test()
