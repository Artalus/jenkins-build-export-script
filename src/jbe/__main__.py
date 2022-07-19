#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple

from jbe.jxml import read_all_workflow_files


class Args(NamedTuple):
    build_dir: Path


def parse_args() -> Args:
    p = ArgumentParser()
    p.add_argument('--build_dir', type=Path)
    return Args(**p.parse_args().__dict__)


def main(args: Args) -> None:
    print(f'build_dir: {args.build_dir.absolute()}')
    xmls = read_all_workflow_files(args.build_dir)
    for x in xmls:
        print(f'--- {x.xpath("/Tag/node/id/text()")[0]}')
        actions = x.xpath('/Tag/actions/*')
        for a in actions:
            print(f'* {a.tag}')
            for kv in a:
                k = kv.tag
                v = kv.text
                print(f'{k}={v}')


def main2() -> None:
    main(parse_args())


if __name__ == '__main__':
    main2()
