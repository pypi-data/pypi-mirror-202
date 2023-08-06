
from typing import List, Dict, Tuple, Union

import random
import time

import math
import random
from collections import namedtuple, deque


from datetime import  datetime
import os
import numpy as np
import subprocess
from queue import Queue
from queue import Empty



def write_async():
    pass


def dtprint(s:str):
    print(s)


def iprint(obj):
    iprint_info(obj)


def iprint_info(obj):
    print("[%s+08:00][INFO][%s]" % (
        datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%dT%H:%M:%S.%f")[0:23],
        obj

    ))


def iprint_warn(obj):
    print("[%s+08:00][WARNING][%s]" % (
        datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%S.%f")[0:23],
        obj

    ))

