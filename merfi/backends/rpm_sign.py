import os
from tambo import Transport
import merfi
from merfi import logger
from merfi import util
from merfi.collector import FileCollector


class RpmSign(object):
    help_menu = 'rpm-sign handler for signing files'
    _help = """
Signs files with rpm-sign. Crawls a given path looking for 'Release' files (by
default)

--key         Name of the key to use
--keyfile     Full path location of the keyfile, defaults to
              /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

Positional Arguments:

[path]        The path to crawl for signing release files. Defaults to current
              working directory
    """
    executable = 'rpm-sign'
    name = 'rpm-sign'

    def __init__(self, argv):
        self.argv = argv
        self.default_keyfile = '/etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release'

    def get_path(self, arguments):
        if os.path.exists(arguments[-1]):
            return os.path.abspath(arguments[-1])
        else:
            return os.path.abspath('.')

    def check_dependencies(self):
        if not util.which(self.executable):
            logger.error('could not find %s' % self.executable)
            raise RuntimeError('%s needs to be installed and available in $PATH' % self.executable)

    def parse_args(self):
        options = ['--key']
        parser = Transport(self.argv, options=options)
        parser.catch_help = self._help
        parser.parse_args()
        self.keyfile = parser.get('--keyfile') or self.default_keyfile
        self.key = parser.get('--key')
        merfi.config['path'] = self.get_path(parser.arguments)
        self.check_dependencies()
        self.sign()

    def sign(self):
        logger.info('Starting path collection, looking for files to sign')
        paths = FileCollector(merfi.config)
        if paths:
            logger.info('%s matching paths found' % len(paths))
            # FIXME: this should spit the actual verified command
            logger.info('will sign with the following commands:')
            logger.info('gpg --armor --detach-sig --output Release.gpg Release')
            logger.info('gpg --clearsign --output InRelease Release')
            logger.info('rpm-sign --key "%s" --detachsign Release --output Release.gpg' % self.key)
            logger.info('rpm-sign --key "%s" --clearsign Release > InRelease' % self.key)
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
                # XXX do actual signing here
                pass
