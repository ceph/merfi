from __future__ import with_statement
import os
import re
import merfi


class RepoCollector(list):

    def __init__(self, path=None, config=None, _eager=True):
        config = config or merfi.config
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
            raise SystemExit('"%s" is a file. Please specify a directory.'
                % self.path)

        # Check whether our root (self.path) is itself a repo.
        if self.is_debian_repo(self.path):
            self.append(self.path)
            return

        # ... if not, walk the tree looking for repos in subdirs.

        # Local is faster
        walk = os.walk
        join = os.path.join
        path = self.path

        for root, dirs, files in walk(path):
            for item in dirs:
                absolute_path = join(root, item)
                if not self.is_debian_repo(item):
                    continue
                self.append(absolute_path)

    def is_debian_repo(self, directory):
        """ Is 'directory' a Debian repository ? """
        join = os.path.join
        isdir = os.path.isdir

        if not isdir(join(directory, 'dists')):
            return False
        if not isdir(join(directory, 'pool')):
            return False
        return True

    @staticmethod
    def debian_release_files(repo):
        """ Find all the "Release" files to be signed within a Debian repo """
        result = []

        # Local is faster
        walk = os.walk
        join = os.path.join
        isfile = os.path.isfile

        dists = join(repo, 'dists')

        # Examine all immediate subdirectories in "dists":
        root, dirs, files = next(walk(dists))
        for dist in dirs:
            release_file = join(root, dist, 'Release')
            if isfile(release_file):
                result.append(release_file)
        return result
