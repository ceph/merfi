from __future__ import with_statement
import os
from glob import glob


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

        if self._is_debian_repo(self.path):
            self.append(DebRepo(self.path))
            return

        # ... if not, walk the tree looking for repos in subdirs.

        # Local is faster
        walk = os.walk
        path = self.path

        for root, dirs, files in walk(path):
            if self._is_debian_repo(root):
                self.append(DebRepo(root))
                continue

    def _is_debian_repo(self, directory):
        """ Is 'directory' a Debian repository ? """
        join = os.path.join
        isdir = os.path.isdir

        if not isdir(join(directory, 'dists')):
            return False
        if not isdir(join(directory, 'pool')):
            return False
        return True
