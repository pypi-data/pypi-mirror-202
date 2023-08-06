# coding=utf-8

# import orjson
import ujson
import json

from typing import Dict, List, NewType

AoD = NewType('AoD', List[Dict])


class Json:

    type2loads = {
        'orjson': ujson.loads,
        'ujson': ujson.loads,
        'json': json.loads}

    type2dumps = {
        'orjson': ujson.dumps,
        'ujson': ujson.dumps,
        'json': json.dumps}

    type2dump = {
        'orjson': json.dump,
        'ujson': json.dump,
        'json': json.dump}

    @classmethod
    def loads(cls, obj, **kwargs):
        json_type = kwargs.get('json_type', 'orjson')
        loads = cls.type2loads.get(json_type)
        return loads(obj)

    @classmethod
    def dumps(cls, obj, **kwargs):
        json_type = kwargs.get('json_type', 'orjson')
        indent = kwargs.get('indent')
        dumps = cls.type2dumps.get(json_type)
        dumps(obj, indent=indent)
        return obj

    @classmethod
    def write(cls, obj, path_, **kwargs):
        json_type = kwargs.get('json', 'orjson')
        indent = kwargs.get('indent', 2)
        dump = cls.type2dump.get(json_type)
        with open(path_, 'w') as fd:
            dump(obj, fd, indent=indent, **kwargs)

    @classmethod
    def read(cls, path_file, **kwargs):
        mode = kwargs.get('mode', 'rb')
        json_type = kwargs.get('json', 'orjson')
        loads = cls.type2loads.get(json_type)
        with open(path_file, mode) as fd:
            return loads(fd.read())
        return None
