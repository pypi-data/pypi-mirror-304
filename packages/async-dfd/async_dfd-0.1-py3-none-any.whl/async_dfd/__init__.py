import json

try:
    with open('./config/async_dfd_config.json', "r") as f:
        print("11231231223")
        ASYNC_DFD_CONFIG = json.load(f)
except FileNotFoundError:
    ASYNC_DFD_CONFIG = {}

from .graph import graph
from .node import node
from .pipeline import pipeline
from .analyser import analyser
import exceptions 

__all__ = ["graph", "node", "pipeline", "analyser", "exceptions"]