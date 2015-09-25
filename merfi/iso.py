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

-o, --output      Custom filename output (defaults to 'isofile').

Positional Arguments:

[source directory]  The path to create the ISO from. Required with no defaults.
"""
    executable = 'genisoimage'
    name = 'iso'

    def parse_args(self):
        options = [['--output', '-o']]
        parser = Transport(self.argv, options=options)
        parser.catch_help = self.help()
        parser.parse_args()
        self.output = parser.get('--output', 'isofile')
        self.source = util.infer_path(parser.unknown_commands)
        self.check_dependency()
        self.make_iso()

    def make_iso(self):
        cmd = ['genisoimage', '-r', '-o', self.output, self.source]
        util.run(cmd)
