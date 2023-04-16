from __future__ import with_statement
import os
from glob import glob


class Rpm(object):
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return os.path.basename(self.path)

    def __eq__(self, other):
        return self.path == other.path

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.path)

    def __hash__(self):
        return hash(self.__repr__())


class Repo(object):
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return self.path == other.path

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.path)

    def __hash__(self):
        return hash(self.__repr__())

    @property
    def releases(self):
        """ DebRepo overrides this. """
        return []

    @property
    def repomd(self):
        """ RpmRepo overrides this. """
        return None

    @property
    def rpms(self):
        """ RpmRepo overrides this. """
        return []


class RpmRepo(Repo):
    @property
    def repomd(self):
        """ Find the repomd.xml file to be signed within a yum repo """
        return os.path.join(self.path, 'repodata/repomd.xml')

    @property
    def rpms(self):
        """ Find all the .rpm files to be signed within a yum repo """
        result = set()
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if name.endswith('.rpm'):
                    path = os.path.join(root, name)
                    result.add(Rpm(path))
        return result


class DebRepo(Repo):
    @property
    def releases(self):
        """ Find all the "Release" files to be signed within a Debian repo """
        match = os.path.join(self.path, 'dists', '*', 'Release')
        return glob(match)


class RepoCollector(list):

    def __init__(self, path=None, config=None, _eager=True):
        self.path = self._abspath(path or '.')
        # making it easier to test
        if _eager:
            self._collect()

    def _abspath(self, path):
        if not path.startswith('/'):
            return os.path.abspath(path)
        return path

    def _collect(self):
        if os.path.isfile(self.path):
            raise SystemExit('"%s" is a file. Please specify a directory.' %
                             self.path)

        # Check whether our root (self.path) is itself a repo.

        if self._is_rpm_repo(self.path):
            self.append(RpmRepo(self.path))
            return

        if self._is_debian_repo(self.path):
            self.append(DebRepo(self.path))
            return

        # ... if not, walk the tree looking for repos in subdirs.

        # Local is faster
        walk = os.walk
        path = self.path

        for root, dirs, files in walk(path):
            if self._is_rpm_repo(root):
                self.append(RpmRepo(root))
                continue
            if self._is_debian_repo(root):
                self.append(DebRepo(root))
                continue

    def _is_rpm_repo(self, directory):
        md = os.path.join(directory, 'repodata', 'repomd.xml')
        if os.path.isfile(md):
            return True
        return False

    def _is_debian_repo(self, directory):
        """ Is 'directory' a Debian repository ? """
        join = os.path.join
        isdir = os.path.isdir

        if not isdir(join(directory, 'dists')):
            return False
        if not isdir(join(directory, 'pool')):
            return False
        return True
