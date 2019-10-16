import argparse

import os
import traceback

import django

from common.core import discovery
from common.kaka.pikachu import PikaChu

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder.settings')
    django.setup()
    parser = argparse.ArgumentParser(description='Go ahead, PikaChu')
    discovery.discover_views()
    discovery.discovery_signal()

    parser.add_argument('pikachu', help='Go ahead, Pikachu', choices=["run", "test"])
    arguments = parser.parse_args()
    pikachu = PikaChu()
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
