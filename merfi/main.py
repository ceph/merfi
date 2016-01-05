import sys

from tambo import Transport
from merfi import backends
from merfi import iso
import merfi
from merfi.decorators import catches


class Merfi(object):
    _help = """
merfi: A utility to find package repositories and sign the metadata with a
given backend signature engine like rpm-sign or gpg.

Version: %s

Global Options:
--log, --logging    Set the level of logging. Acceptable values:
                    debug, warning, error, critical
--check             Don't perform any actions, attempt to determine what would
                    happen and spit output as similar as possible

Sub Commands:
%s

    """

    mapper = {
        'rpm-sign': backends.rpm_sign.RpmSign,
        'gpg': backends.gpg.Gpg,
        'iso': iso.Iso
    }

    def __init__(self, argv=None, parse=True):
        if argv is None:
            argv = sys.argv
        if parse:
            self.main(argv)

    def help(self):
        sub_help = '\n'.join(['%-19s %s' % (
            sub.name, getattr(sub, 'help_menu', ''))
            for sub in self.mapper.values()])
        return self._help % (merfi.__version__, sub_help)

    @catches((RuntimeError, KeyboardInterrupt))
    def main(self, argv):
        options = [['--log', '--logging']]
        parser = Transport(argv, mapper=self.mapper,
                           options=options, check_help=False,
                           check_version=False)
        parser.parse_args()
        merfi.config['verbosity'] = parser.get('--log', 'info')
        merfi.config['check'] = parser.has('--check')
        parser.catch_help = self.help()
        parser.catch_version = merfi.__version__
        parser.mapper = self.mapper
        if len(argv) <= 1:
            return parser.print_help()
        parser.dispatch()
        parser.catches_help()
        parser.catches_version()
