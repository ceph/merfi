from __future__ import with_statement
import os
import re


class FileCollector(list):

    def __init__(self, path, config=None):
        config = config or {}
        self.user_match = config.get('match')
        self.case_insensitive = config.get('ignorecase')
        self.path = path
        self._collect()

    @property
    def valid_name(self):
        fallback = re.compile(r'Release$')
        if not self.user_match:
            return fallback
        else:
            try:
                if self.case_insensitive:
                    return re.compile(self.user_match, re.IGNORECASE)
                return re.compile(self.user_match)
            except Exception, msg:
                raise SystemExit('Could not compile regex, error was: %s' % msg)

    def _collect(self):
        if os.path.isfile(self.path):
            self.append(self.path)
            return

        # Local is faster
        walk = os.walk
        join = os.path.join
        path = self.path

        for root, dirs, files in walk(path):
            for item in files:
                absolute_path = join(root, item)
                if not self.valid_module_name.match(item):
                    continue
                self.append(absolute_path)
