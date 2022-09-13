#!/usr/bin/env python3

from argparse import ArgumentParser
import json
from pathlib import Path
from pprint import pprint
from typing import NamedTuple

import requests

from jbe.json_repr import NodeData
from jbe.jxml import NodeXml, read_all_workflow_files


class Args(NamedTuple):
    build_dir: Path
    post_url: str


def parse_args() -> Args:
    p = ArgumentParser()
    p.add_argument('--build_dir', type=Path)
    p.add_argument('--post_url')
    return Args(**p.parse_args().__dict__)


def main(args: Args) -> None:
    print(f'build_dir: {args.build_dir.absolute()}')
    xmls = read_all_workflow_files(args.build_dir)
    xml_nodes = [NodeXml.from_xml(x) for x in xmls]
    xml_nodes_dict = {x.id: x for x in xml_nodes}
    json_nodes = [NodeData.from_xml(x, xml_nodes_dict) for x in xml_nodes]
    payload = {
        "job": "e",
        "buildName": "#7",
        "buildFullName": "e #7",
        "buildNumber": 7,
        "buildUrl": "http://omgwtf.local/job/e/7",
        "buildResult": "SUCCESS",
        "buildParameters": {
            "PASS": "*CENSORED*"
        },
        "nodes": [n.to_json() for n in json_nodes]
    }
    resp = requests.post(args.post_url, json=payload)
    print(resp)
    print(resp.content)

def main2() -> None:
    main(parse_args())


if __name__ == '__main__':
    main2()
