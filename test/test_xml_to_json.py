from typing import List, cast

import lxml.etree as ET
from lxml.etree import _Element as XML

from jbe.jxml import ActionData, NodeXml, arguments_entries_to_dict

def test_action_data_from_xml() -> None:
    with open(td_file('smalljob', 1, 2)) as f:
        xml = ET.parse(f)

    actions = cast(List[XML], xml.xpath('/Tag/actions/*'))
    assert isinstance(actions, list)

    ads = [ActionData.from_xml(x) for x in actions]
    assert len(ads) == 1

    ad = ads[0]
    assert ad.type == 'TimingAction'
    assert ad.fulltype == 'wf.a.TimingAction'
    assert ad.data == dict(startTime='1658432251468')


def test_node_from_xml() -> None:
    with open(td_file('folder/jobs/biggerjob', 4, 4)) as f:
        xml = ET.parse(f)

    nd = NodeXml.from_xml(xml)
    assert nd.id == '4'
    assert nd.parents == ['3']
    assert nd.type == 'StepAtomNode'
    assert nd.start_id is None
    assert sorted(nd.actions) == sorted([
        ActionData(
            type='ArgumentsActionImpl',
            fulltype='cps.a.ArgumentsActionImpl',
            data=dict(
                message='${PASSWORD}'
            )
        ),
        ActionData(
            type='LogStorageAction',
            fulltype='s.a.LogStorageAction',
            data={}
        ),
        ActionData(
            type='TimingAction',
            fulltype='wf.a.TimingAction',
            data=dict(
                startTime='1658432889682'
            )
        ),
    ])


def test_entries_dict() -> None:
    xml = ET.fromstring('''
        <arguments>
            <entry>
                <string>script</string>
                <string>ls</string>
            </entry>
            <entry>
                <string>label</string>
                <string>kek</string>
            </entry>
        </arguments>'''
    )
    assert arguments_entries_to_dict(xml.xpath('/arguments/entry')) == dict(
        script='ls',
        label='kek'
    )
    xml = ET.fromstring('<arguments />'
    )
    assert arguments_entries_to_dict(xml.xpath('/arguments/entry')) == dict()


def td_file(path: str, build: int, step: int) -> str:
    return f'test-data/{path}/builds/{build}/workflow/{step}.xml'
