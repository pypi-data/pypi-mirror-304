from gevent import monkey
monkey.patch_all()

import json

try:
    with open('./config/async_dfd_config.json', "r") as f:
        ASYNC_DFD_CONFIG = json.load(f)
except FileNotFoundError:
    ASYNC_DFD_CONFIG = {}

from .node import Node
from .node_group import node_group
from .analyser import analyser

__all__ = ["node_group", "Node", "analyser", "exceptions", "decorator"]