from pathlib import Path
from typing import Any, Dict, List, Literal, NamedTuple, Union

import lxml.etree as ET
from lxml.etree import _ElementTree as XMLT, _Element as XML

def read_all_workflow_files(build_dir: Path) -> List[XMLT]:
    result = []
    for x in (build_dir / 'workflow').glob('*.xml'):
        result.append(ET.parse(x))
    return result

class ActionData(NamedTuple):
    type: str
    fulltype: str
    data: Any

    @staticmethod
    def from_xml(elem: XML) -> 'ActionData':
        tag: str = elem.tag
        clazz = tag.split('.')[-1]

        return ActionData(
            type=clazz,
            fulltype=tag,
            data=elem2dict(elem),
        )

NodeType = Literal[
    'Unknown',
    'FlowStart',
    'FlowEnd',
    'StepAtom',
    'StepStart',
    'StepEnd',
]


# (c) pieterdd https://gist.github.com/jacobian/795571?permalink_comment_id=2810160#gistcomment-2810160
def elem2dict(node: XML) -> Dict[str, Any]:
    """
    Convert an lxml.etree node tree into a dict.
    """
    result: Dict[str, Any] = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            result[key] = element.text
        else:
            result[key] = elem2dict(element)

    return result
