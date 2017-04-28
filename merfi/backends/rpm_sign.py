import os
import shutil
from tambo import Transport
import merfi
from merfi import logger
from merfi import util
from merfi.collector import RepoCollector
from merfi.backends import base


class RpmSign(base.BaseBackend):
    help_menu = 'rpm-sign handler for signing files'
    _help = """
Signs files with rpm-sign. Crawls a given path looking for Debian repos.

%s

Options

--key         Name of the key to use (see rpm-sign --list-keys)
--keyfile     Full path location of the public keyfile, for example
              /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
              or /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta
--nat         A NAT is between this system and the signing server.

Positional Arguments:

[path]        The path to crawl for signing repos. Defaults to current
              working directory
    """
    executable = 'rpm-sign'
    name = 'rpm-sign'
    options = ['--key', '--keyfile', '--nat']

    def clear_sign(self, path, command):
        """
        When doing a "clearsign" with rpm-sign, the output goes to stdout, so
        that needs to be captured and written to the default output file for
        clear signed signatures (InRelease).
        """
        logger.info('signing: %s' % path)
        out, err, code = util.run_output(command)
        absolute_directory = os.path.dirname(os.path.abspath(path))
        with open(os.path.join(absolute_directory, 'InRelease'), 'w') as f:
            f.write(out)

    def detached(self, command):
        return util.run(command)

    def sign(self):
        self.keyfile = self.parser.get('--keyfile')
        if self.keyfile and not os.path.isfile(self.keyfile):
            raise RuntimeError('%s is not a file' % self.keyfile)
        self.key = self.parser.get('--key')
        if not self.key:
            raise RuntimeError('specify a --key for signing')
        logger.info('Starting path collection, looking for files to sign')
        repos = RepoCollector(self.path)
        paths = repos.debian_release_files

        if paths:
            logger.info('%s matching paths found' % len(paths))
            # FIXME: this should spit the actual verified command
            logger.info('will sign with the following commands:')
            logger.info('rpm-sign --key "%s" --detachsign Release --output Release.gpg' % self.key)
            logger.info('rpm-sign --key "%s" --clearsign Release --output InRelease' % self.key)
        else:
            logger.warning('No paths found that matched')

        for path in paths:
            if merfi.config.get('check'):
                new_gpg_path = path.split('Release')[0]+'Release.gpg'
                new_in_path = path.split('Release')[0]+'InRelease'
                logger.info('[CHECKMODE] signing: %s' % path)
                logger.info('[CHECKMODE] signed: %s' % new_gpg_path)
                logger.info('[CHECKMODE] signed: %s' % new_in_path)
            else:
                os.chdir(os.path.dirname(path))
                detached = ['rpm-sign', '--key', self.key, '--detachsign', 'Release', '--output', 'Release.gpg']
                clearsign = ['rpm-sign', '--key', self.key, '--clearsign', 'Release']
                if self.parser.has('--nat'):
                    detached.insert( 1, '--nat')
                    clearsign.insert( 1, '--nat')
                logger.info('signing: %s' % path)
                self.detached(detached)
                self.clear_sign(path, clearsign)

        if self.keyfile:
            logger.info('using keyfile "%s" as release.asc' % self.keyfile)
            for repo in repos:
                logger.info('placing release.asc in %s' % repo)
                if merfi.config.get('check'):
                    logger.info('[CHECKMODE] writing release.asc')
                else:
                    shutil.copyfile(
                        self.keyfile,
                        os.path.join(repo.path, 'release.asc'))
