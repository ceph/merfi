import os
from tambo import Transport
import merfi
from merfi import logger
from merfi import util
from merfi.collector import FileCollector
from merfi.backends import base


class RpmSign(base.BaseBackend):
    help_menu = 'rpm-sign handler for signing files'
    _help = """
Signs files with rpm-sign. Crawls a given path looking for 'Release' files (by
default)

%s

Options

--key         Name of the key to use
--keyfile     Full path location of the keyfile, defaults to
              /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

Positional Arguments:

[path]        The path to crawl for signing release files. Defaults to current
              working directory
    """
    executable = 'rpm-sign'
    name = 'rpm-sign'
    options = ['--key']

    def sign(self):
        logger.info('Starting path collection, looking for files to sign')
        self.keyfile = self.parser.get('--keyfile', 'Release.gpg')
        self.key = self.parser.get('--key')
        paths = FileCollector(self.path)

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
