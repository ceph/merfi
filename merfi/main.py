import sys

from tambo import Transport
from merfi import logger
from merfi import backends
import merfi
from merfi.decorators import catches


class Merfi(object):
    _help = """
merfi: A utility to find Release files and sign them with a given backend
signature engine like rpm-sign or gpg.

Version: %s

Global Options:
--log, --logging    Set the level of logging. Acceptable values:
                    debug, warning, error, critical

Sub Commands:
rpm-sign            Uses the `rpm-sign` utility to sign files
gpg                 Uses `gpg` to sign files

    """

    mapper = {
        'rpm-sign': backends.rpm_sign.RpmSign,
        'gpg': backends.gpg.Gpg
    }

    def __init__(self, argv=None, parse=True):
        self.plugin_help = "No plugins found/loaded"
        if argv is None:
            argv = sys.argv
        if parse:
            self.main(argv)

    def help(self):
        return self._help % (merfi.__version__)

    @catches(KeyboardInterrupt)
    def main(self, argv):
        options = [['--log', '--logging']]
        parser = Transport(argv, mapper=self.mapper,
                           options=options, check_help=False,
                           check_version=False)
        parser.parse_args()
        merfi.config['verbosity'] = parser.get('--log', 'info')
        parser.catch_help = self.help()
        parser.catch_version = merfi.__version__
        parser.mapper = self.mapper
        if len(argv) <= 1:
            return parser.print_help()
        parser.dispatch()
        parser.catches_help()
        parser.catches_version()
