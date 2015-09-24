import os
from tambo import Transport
from merfi.collector import FileCollector
import merfi
from merfi import logger
from merfi import util


class Iso(object):
    help_menu = 'simple ISO manipulation'
    _help = """
A very simple interface to create ISOs with some sane defaults (like ensure
source directory has proper read permissions).

Default behavior will perform these actions on a source directory::

    genisoimage -r -o isofile {source directory}

Options:

--output      Custom filename output (defaults to 'isofile').

Positional Arguments:

[source directory]  The path to create the ISO from. Required with no defaults.
"""
    executable = 'genisoimage'
    name = 'iso'

    def __init__(self, argv):
        self.argv = argv

    def parse_args(self):
        pass
