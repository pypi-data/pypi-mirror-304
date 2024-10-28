import logging

from ..pipeline import Pipeline

logger = logging.getLogger(__name__)


class CyclePipeline(Pipeline):

    def __init__(self, all_nodes, head_output=False):
        super().__init__(all_nodes=all_nodes)
        self.tail.set_destination(self.head)
        if head_output:
            self.tail = self.head
