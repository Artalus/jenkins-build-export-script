from typing import List, cast

import lxml.etree as ET
from lxml.etree import _Element as XML

from jbe.jxml import ActionData

def test_tmp_flow_node_1_2() -> None:
    with open(td_file(1, 2)) as f:
        xml = ET.parse(f)

    actions = cast(List[XML], xml.xpath('/Tag/actions/*'))
    assert isinstance(actions, list)

    ads = [ActionData.from_xml(x) for x in actions]
    assert len(ads) == 1

    ad = ads[0]
    assert len(ad) == 1
    assert ad.type == 'TimingAction'
    assert isinstance(ad.data, dict)
    assert ad.data['startTime'] == '1658136900281'

def td_file(build: int, step: int) -> str:
    return f'test-data/jobs/sandbox/jobs/tmp-flow-nodes/builds/{build}/workflow/{step}.xml'
