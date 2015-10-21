from __future__ import with_statement
import os
import re
import merfi


class FileCollector(list):

    def __init__(self, path=None, config=None, _eager=True):
        config = config or merfi.config
        self.path = self._abspath(path or '.')
        # making it easier to test
        if _eager:
            self._collect()

    def _abspath(self, path):
        if not path.startswith('/'):
            return os.path.abspath(path)
        return path

    def _collect(self):
        if os.path.isfile(self.path):
            self.append(self.path)
            return

        # Local is faster
        walk = os.walk
        join = os.path.join
        path = self.path

        valid_name = re.compile(r'Release$')
        for root, dirs, files in walk(path):
            for item in files:
                absolute_path = join(root, item)
                if not valid_name.match(item):
                    continue
                self.append(absolute_path)
