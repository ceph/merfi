import os
from merfi.collector import RepoCollector
import merfi
from merfi import logger, util
from merfi.backends import base


class Gpg(base.BaseBackend):
    help_menu = 'gpg handler for signing files'
    _help = """
Signs files with gpg. Crawls a given path looking for Debian repos.

Default behavior will perform these actions on 'Release' files:

    gpg --armor --detach-sig --output Release.gpg Release
    gpg --clearsign --output InRelease Release

%s

Options:

Positional Arguments:

[path]        The path to crawl for signing repos. Defaults to current
              working directory
"""
    executable = 'gpg'
    name = 'gpg'

    def sign(self):
        logger.info('Starting path collection, looking for files to sign')
        repos = RepoCollector(self.path)

        if repos:
            logger.info('%s repos found' % len(repos))
        else:
            logger.warning('No paths found that matched')

        for repo in repos:
            # Debian "Release" files:
            for path in repo.releases:
                self.sign_release(path)

    def sign_release(self, path):
        """ Sign a "Release" file from a Debian repo.  """
        if merfi.config.get('check'):
            new_gpg_path = path.split('Release')[0]+'Release.gpg'
            new_in_path = path.split('Release')[0]+'InRelease'
            logger.info('[CHECKMODE] signing: %s' % path)
            logger.info('[CHECKMODE] signed: %s' % new_gpg_path)
            logger.info('[CHECKMODE] signed: %s' % new_in_path)
        else:
            os.chdir(os.path.dirname(path))
            detached = ['gpg', '--batch', '--yes', '--armor', '--detach-sig',
                        '--output', 'Release.gpg', 'Release']
            clearsign = ['gpg', '--batch', '--yes', '--clearsign', '--output',
                         'InRelease', 'Release']
            logger.info('signing: %s' % path)
            util.run(detached)
            util.run(clearsign)
