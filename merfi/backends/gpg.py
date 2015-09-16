import os
from tambo import Transport
from merfi.collector import FileCollector
import merfi


class Gpg(object):
    help_menu = 'gpg handler for signing files'
    _help = """
Signs files with gpg. Crawls a given path looking for 'Release' files (by
default)

--output      Custom filename output (vs. $filename.asc).
              Defaults to Release.gpg

Positional Arguments:

[path]        The path to crawl for signing release files. Defaults to current
              working directory
"""

    def __init__(self, argv):
        self.argv = argv
        self.default_keyfile = '/etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release'

    def get_path(self, arguments):
        if os.path.exists(arguments[-1]):
            return os.path.abspath(arguments[-1])
        else:
            return os.path.abspath('.')

    def parse_args(self):
        parser = Transport(self.argv)
        parser.catch_help = self._help
        parser.parse_args()
        file_output = parser.get('--output') or self.default_keyfile
        merfi.config['path'] = self.get_path(parser.arguments)
        self.sign()

    def sign(self):
        paths = FileCollector(merfi.config)
        for path in paths:
            print path
