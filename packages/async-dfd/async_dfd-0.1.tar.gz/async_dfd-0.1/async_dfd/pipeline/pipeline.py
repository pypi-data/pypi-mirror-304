import logging
from typing import List

from ..node import Node
from ..interface import NodeGroup, NodeTransferable

logger = logging.getLogger(__name__)


class Pipeline(NodeGroup, NodeTransferable):
    def __init__(
        self,
        all_nodes: List[Node],
    ):
        super().__init__(all_nodes=all_nodes)
        self.head = all_nodes[0]
        self.tail = all_nodes[-1]
        self.heads = {self.head.__name__: self.head}
        self.tails = {self.tail.__name__: self.tail}

    def _connect_nodes(self):
        former = None
        for node in self.all_nodes.values():
            if former is None:
                former = node
                continue
            else:
                logger.info(f"connect {former.__name__} to {node.__name__}")
                former.set_destination(node)
                former = node

    def start(self):
        assert (
            len(self.heads) == 1
        ), f"Only one head node is allowed in the pipeline {self.__name__}"
        assert (
            len(self.tails) == 1
        ), f"Only one tail node is allowed in the pipeline {self.__name__}"
        return super().start()

    def put(self, data):
        self.head.put(data)

    def set_destination(self, dst_node: Node):
        self.tail.set_destination(dst_node)

    @property
    def criteria(self):
        return self.head.criteria
