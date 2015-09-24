import os
import pytest
from merfi.collector import FileCollector

class TestFileCollector(object):

    def test_simple_tree(self, repotree):
        paths = FileCollector({'path': repotree})
        expected = [
            os.path.join(repotree, 'dists', 'precise', 'Release'),
            os.path.join(repotree, 'dists', 'trusty',  'Release'),
        ]
        assert set(paths) == set(expected)
