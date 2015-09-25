from tambo import Transport
from merfi.collector import FileCollector
import merfi
from merfi import logger, util, base


class Iso(base.BaseCommand):
    help_menu = 'simple ISO manipulation'
    _help = """
A very simple interface to create ISOs with some sane defaults (like ensure
source directory has proper read permissions).

Default behavior will perform these actions on a source directory::

    genisoimage -r -o isofile {source directory}

%s

Options:

--output      Custom filename output (defaults to 'isofile').

Positional Arguments:

[source directory]  The path to create the ISO from. Required with no defaults.
"""
    executable = 'genisoimage'
    name = 'iso'

    def parse_args(self):
        parser = Transport(self.argv)
        parser.catch_help = self.help()
        parser.parse_args()
        self.check_dependency()
