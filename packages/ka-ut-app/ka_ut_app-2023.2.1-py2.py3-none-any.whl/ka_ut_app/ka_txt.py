# coding=utf-8

import pprint

from typing import Dict


class Txt:

    @classmethod
    def write(dic: Dict, path: str, indent: int = 2) -> None:
        data = pprint.pformat(dic, indent=indent)
        with open(path, 'w') as fd:
            fd.write(data)
