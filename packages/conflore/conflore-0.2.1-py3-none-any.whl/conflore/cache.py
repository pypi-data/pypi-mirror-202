"""
TODO: not used yet.
"""
import atexit
import os
import tempfile

from .load_and_dump import dumps
from .load_and_dump import loads


class Cache:
    
    def __init__(self, _cache_file: str = None):
        # self.__self_protected = False
        self._dict = {}
        self._file = _cache_file or tempfile.mktemp()
        if os.path.exists(self._file):
            self._dict.update(loads(self._file))
        atexit.register(self._remove)
        # self.__self_protected = True
    
    def __getattr__(self, item):
        preserved_keys = ('_dict', '_file', '_remove', 'save', 'update')
        if isinstance(item, str):
            if not (item.startswith('__') or item in preserved_keys):
                return self._dict[item]
        return super().__getattribute__(item)
    
    def __setattr__(self, key, value):
        preserved_keys = ('_dict', '_file', '_remove', 'save', 'update')
        if isinstance(key, str):
            if not (key.startswith('__') or key in preserved_keys):
                self._dict[key] = value
                self.save()
                return
        super().__setattr__(key, value)
    
    def update(self, kwargs: dict) -> None:
        self._dict.update(kwargs)
        self.save()
    
    def save(self) -> None:
        dumps(self._dict, self._file)
        print('cache saved.')
    
    def _remove(self) -> None:
        if os.path.exists(self._file):
            os.remove(self._file)
            print('cache removed.')


cache = Cache()
