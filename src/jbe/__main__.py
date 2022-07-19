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
    print(read_all_workflow_files(args.build_dir))


def main2() -> None:
    main(parse_args())


if __name__ == '__main__':
    main2()
