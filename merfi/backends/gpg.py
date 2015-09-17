import os
from tambo import Transport
from merfi.collector import FileCollector
import merfi
from merfi import logger
from merfi import util


class Gpg(object):
    help_menu = 'gpg handler for signing files'
    _help = """
Signs files with gpg. Crawls a given path looking for 'Release' files (by
default)

Default behavior will perform these actions on 'Release' files::

    gpg --armor --detach-sig --output Release.gpg Release
    gpg --clearsign --output InRelease Release

Options:

--output      Custom filename output (vs. $filename.asc).
              Defaults to Release.gpg

Positional Arguments:

[path]        The path to crawl for signing release files. Defaults to current
              working directory
"""
    executable = 'gpg'

    def __init__(self, argv):
        self.argv = argv
        self.default_keyfile = '/etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release'

    def get_path(self, arguments):
        try:
            path = arguments[-1]
        except IndexError:
            path = '.'
        if os.path.exists(path):
            return os.path.abspath(path)
        else:
            return os.path.abspath('.')

    def parse_args(self):
        parser = Transport(self.argv)
        parser.catch_help = self._help
        parser.parse_args()
        file_output = parser.get('--output') or self.default_keyfile
        merfi.config['path'] = self.get_path(parser.arguments)
        self.check_dependencies()
        self.sign(file_output)

    def check_dependencies(self):
        if not util.which(self.executable):
            logger.error('could not find %s' % self.executable)
            raise RuntimeError('%s needs to be installed and available in $PATH' % self.executable)

    def sign(self, file_output):
        logger.info('Starting path collection, looking for files to sign')
        paths = FileCollector(merfi.config)
        if paths:
            logger.info('%s matching paths found' % len(paths))
            # FIXME: this should spit the actual verified command
            logger.info('will sign with the following commands:')
            logger.info('gpg --armor --detach-sig --output Release.gpg Release')
            logger.info('gpg --clearsign --output InRelease Release')
        else:
            logger.warning('No paths found that matched')

        for path in paths:
            if merfi.config['check']:
                new_gpg_path = path.split('Release')[0]+'Release.gpg'
                new_in_path = path.split('Release')[0]+'InRelease'
                logger.info('[CHECKMODE] signing: %s' % path)
                logger.info('[CHECKMODE] signed: %s' % new_gpg_path)
                logger.info('[CHECKMODE] signed: %s' % new_in_path)
            else:
                os.chdir(os.path.dirname(path))
                # FIXME: this needs to allow for configurable output name
                detached = ['gpg', '--armor', '--detach-sig', '--output', 'Release.gpg', 'Release']
                clearsign = ['gpg', '--clearsign', '--output', 'InRelease', 'Release']
                logger.info('signing: %s' % path)
                util.run(detached)
                util.run(clearsign)
