from hashlib import sha256
import os
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
    sha256sum isofile > isofile.SHA256SUM

%s

Options:

-o, --output      Custom filename output (defaults to 'isofile').

Positional Arguments:

[source directory]  The path to create the ISO from. Required with no defaults.
"""
    executable = 'genisoimage'
    name = 'iso'

    def parse_args(self, argv=None):
        """ pass argv during testing """
        if argv is None:
            argv = self.argv
        options = [['--output', '-o']]
        parser = Transport(argv, options=options)
        parser.catch_help = self.help()
        parser.parse_args()
        self.output = parser.get('--output', 'isofile')
        self.source = util.infer_path(parser.unknown_commands)
        self.check_dependency()
        self.make_iso()
        self.make_sha256sum()

    def make_iso(self):
        cmd = ['genisoimage', '-r', '-o', self.output, self.source]
        util.run(cmd)

    def make_sha256sum(self):
        chsum = sha256()
        self.output_checksum = self.output + '.SHA256SUM'
        with open(self.output, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                chsum.update(chunk)
        digest = chsum.hexdigest()
        with open(self.output_checksum, 'w') as chsumf:
            chsumf.write("%s  %s\n" % (digest, os.path.basename(self.output)))
