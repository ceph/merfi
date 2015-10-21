import os
import pytest
from merfi.collector import FileCollector


class TestFileCollector(object):

    def setup(self):
        self.paths = FileCollector(path='/', _eager=False)

    def test_simple_tree(self, repotree):
        paths = FileCollector(path=repotree)
        expected = [
            os.path.join(repotree, 'dists', 'precise', 'Release'),
            os.path.join(repotree, 'dists', 'trusty',  'Release'),
        ]
        assert set(paths) == set(expected)

    def test_path_is_absolute(self):
        assert self.paths._abspath('/') == '/'

    def test_path_is_not_absolute(self):
        assert self.paths._abspath('directory').startswith('/')
