from pprint import pprint
from enum import Enum
import random

DEBUG = False

def debug_print(data):
    if DEBUG:
        pprint(data)


def get_random_hex(length):
    return ''.join([random.choice("0123456789abcdef") for _ in range(length)])


def get_random_device_id():
    return get_random_hex(16) + "--" + str(random.randrange(100000000, 999999999))


class OperationMode(Enum):
    DOWNLOAD = "download"
    SEARCH = "search"
