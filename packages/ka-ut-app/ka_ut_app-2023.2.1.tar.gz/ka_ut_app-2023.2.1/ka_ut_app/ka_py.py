# coding=utf-8

# from typing import Dict


class Py:

    @staticmethod
    def write(obj, path):
        with open(path, 'w') as fd:
            for line in obj:
                fd.write(line)
