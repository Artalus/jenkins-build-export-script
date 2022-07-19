#!/usr/bin/env python3

from argparse import ArgumentParser
from typing import NamedTuple


class Args(NamedTuple):
    pass


def parse_args() -> Args:
    p = ArgumentParser()
    return Args(**p.parse_args().__dict__)


def main(args: Args) -> None:
    print('jbe')


def main2() -> None:
    main(parse_args())


if __name__ == '__main__':
    main2()
