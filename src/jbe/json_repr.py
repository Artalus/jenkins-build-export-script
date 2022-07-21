from typing import Dict, List, NamedTuple, Optional

from jbe.jxml import ActionData, NodeXml


class NodeData(NamedTuple):
    '''
    A higher level abstraction about NodeFlow xml, closer to an actual NodeFlow object
    from Java.
    '''
    id: str
    timestamp: int
    enclosing: Optional[str]
    type: str
    depth: int
    # parent is a node that was executed BEFORE this one
    parents: List[str]
    # enclosing is a node INSIDE which this node happens
    enclosings: List[str]
    startNode: Optional[str]
    actions: List[ActionData]

    @staticmethod
    def from_xml(this: NodeXml, everything: Dict[str, NodeXml]) -> 'NodeData':
        enclosings = NodeData.extract_enclosings(this, everything)
        return NodeData(
            id=this.id,
            timestamp=NodeData.extract_timestamp(this.actions),
            enclosing=enclosings[0] if enclosings else None,
            type=this.type.rstrip('Node'),
            enclosings=enclosings,
            depth=NodeData.calculate_depth(this, everything),
            parents=[], # TODO: is this even needed?
            startNode=this.start_id,
            actions=this.actions,
        )

    @staticmethod
    def extract_enclosings(this: NodeXml, everything: Dict[str, NodeXml]) -> List[str]:
        # FIXME: parse all parents in search of BodySomething
        return this.parents

    @staticmethod
    def extract_timestamp(actions: List[ActionData]) -> int:
        data: Dict[str, str] = next(a for a in actions if a.type == 'TimingAction').data
        return int(data['startTime'])

    @staticmethod
    def calculate_depth(this: NodeXml, everything: Dict[str, NodeXml]) -> int:
        # FIXME: DOES NOT WORK, should traverse parsed enclosings instead of original parents
        depth = 0
        INFINITE_LOOP_LIMIT = 1000
        while this.parents:
            if depth > INFINITE_LOOP_LIMIT:
                raise RuntimeError(f'absurd depth > {INFINITE_LOOP_LIMIT}, possibly an infinite loop')
            depth += 1
            this = everything[this.parents[0]]
        return depth
