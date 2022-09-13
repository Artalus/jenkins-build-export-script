"""
Describes classes used for typization of FlowNode objects, serialized by Jenkins
into `workflolw/#.xml`. Mainly used to be able to test that xml contents are
parsed as they are meant to be.

"""
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, NamedTuple, Optional, Union, cast

import lxml.etree as ET
from lxml.etree import _ElementTree as XMLT, _Element as XML


def read_all_workflow_files(build_dir: Path) -> List[XMLT]:
    result = []
    for x in (build_dir / 'workflow').glob('*.xml'):
        result.append(ET.parse(x))
    return result

class ActionData(NamedTuple):
    """
    Describes entries in <actions>...</actions> block of single FlowNode XML
    """
    type: str
    fullType: str
    data: Any

    @staticmethod
    def from_xml(elem: XML) -> 'ActionData':
        tag: str = elem.tag
        clazz = tag.split('.')[-1]

        if clazz == 'ArgumentsActionImpl':
            entries = cast(List[XML], elem.xpath('./arguments/entry'))
            data = arguments_entries_to_dict(entries)
        else:
            data = elem2dict(elem)

        return ActionData(
            type=clazz,
            fullType=tag,
            data=data,
        )

class NodeXml(NamedTuple):
    """
    Describes whole <Tag> object from serialized FlowNode xml - but nothing
    more than xml contents. Leaves depth calculation and other JSON representaion
    compatibility for higher abstraction levels
    """
    id: str
    type: str
    parents: List[str]
    actions: List[ActionData]
    start_id: Optional[str]
    # TODO: add descriptor???

    @staticmethod
    def from_xml(e: XML) -> 'NodeXml':
        clazz = cast(List[str], e.xpath('/Tag/node/@class'))[0]
        idd = cast(List[str], e.xpath('/Tag/node/id/text()'))
        parents = cast(List[str], e.xpath('/Tag/node/parentIds/*/text()'))
        actions = cast(List[XML], e.xpath('/Tag/actions/*'))
        start_id = cast(List[str], e.xpath('/Tag/node/startId/text()'))
        return NodeXml(
            id=idd[0],
            type=clazz.split('.')[-1],
            parents=parents,
            actions=[ActionData.from_xml(x) for x in actions],
            start_id = start_id[0] if start_id else None,
        )
        # parents =



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

def arguments_entries_to_dict(entries: Iterable[XML]) -> Dict[str, str]:
    """
    For <ArgumentsActionImpl>, converts its <arguments> list into a simple arg=value dictionary
    FIXME: DOES NOT WORK for anything other than simple string+string entries
    """
    result = dict()
    for e in entries:
        strings = cast(List[XML], e.xpath('./string'))
        k, v = strings
        assert k.text
        assert v.text
        result[k.text] = v.text
    return result
