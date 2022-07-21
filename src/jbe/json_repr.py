from enum import Enum
from os import times
import re
from typing import Dict, List, NamedTuple, Optional

from jbe.jxml import ActionData, NodeXml


class NodeData(NamedTuple):
    id: str
    timestamp: int
    enclosing: Optional[str]
    type: str
    depth: int
    parents: List[str]
    enclosings: List[str]
    startNode: Optional[str]
    actions: List[ActionData]

    @staticmethod
    def from_xml(this: NodeXml, everything: Dict[str, NodeXml]) -> 'NodeData':
        timestamp = next(a for a in this.actions if a.type == 'TimingAction').data['startTime']
        enclosings = this.parents
        depth = NodeData.calculate_depth(this, everything)
        return NodeData(
            id=this.id,
            timestamp=timestamp,
            enclosing=enclosings[0] if enclosings else None,
            type=this.type.rstrip('Node'),
            enclosings=enclosings,
            depth=depth,
            parents=[], # TODO: is this even needed?
            startNode=this.start_id,
            actions=this.actions,
        )

    @staticmethod
    def calculate_depth(this: NodeXml, everything: Dict[str, NodeXml]) -> int:
        depth = 0
        INFINITE_LOOP_LIMIT = 1000
        while this.parents:
            if depth > INFINITE_LOOP_LIMIT:
                raise RuntimeError(f'absurd depth > {INFINITE_LOOP_LIMIT}, possibly an infinite loop')
            depth += 1
            this = everything[this.parents[0]]
        return depth
