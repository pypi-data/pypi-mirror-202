# coding=utf-8

from typing import Any

from yaml import load, dump, safe_load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader
try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper


class Yaml:

    """ Manage Object to Yaml file affilitation
    """
    @staticmethod
    def load_with_loader(string: str) -> None | Any:
        return load(string, Loader=Loader)

    @staticmethod
    def load_with_safeloader(string: str) -> None | Any:
        return load(string, Loader=SafeLoader)

    @staticmethod
    def safe_load(string: str, **kwargs) -> None | Any:
        return safe_load(string, **kwargs)
        # return load(string, Loader=yaml.SafeLoader)

    @staticmethod
    def read(path: str) -> None | Any:
        with open(path) as fd:
            # The Loader parameter handles the conversion from YAML
            # scalar values to Python object format
            return load(fd, Loader=SafeLoader)
        return None

    @staticmethod
    def write(obj: Any, path: str) -> None:
        with open(path, 'w') as fd:
            dump(
                obj, fd,
                Dumper=SafeDumper,
                sort_keys=False,
                indent=4,
                default_flow_style=False
            )
            #   block_seq_indent=2,
