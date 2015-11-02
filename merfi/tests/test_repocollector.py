from merfi.collector import RepoCollector
from os.path import join, dirname


class TestRepoCollector(object):

    def setup(self):
        self.paths = RepoCollector(path='/', _eager=False)

    def test_simple_tree(self, repotree):
        paths = RepoCollector(path=repotree)
        # The root of the repotree fixture is itself a repository.
        expected = [ repotree ]
        assert set(paths) == set(expected)

    def test_path_is_absolute(self):
        assert self.paths._abspath('/') == '/'

    def test_path_is_not_absolute(self):
        assert self.paths._abspath('directory').startswith('/')

    def test_debian_release_files(self, repotree):
        paths = RepoCollector(repotree)
        release_files = paths.debian_release_files
        # The root of the repotree fixture is itself a repository.
        expected = [
            join(repotree, 'dists', 'trusty', 'Release'),
            join(repotree, 'dists', 'precise', 'Release'),
        ]
        assert set(release_files) == set(expected)

    def test_debian_nested_release_files(self, nested_repotree):
        # go one level up
        path = dirname(nested_repotree)
        paths = RepoCollector(path)
        release_files = paths.debian_release_files
        expected = [
            join(nested_repotree, 'dists', 'trusty', 'Release'),
            join(nested_repotree, 'dists', 'precise', 'Release'),
        ]
        assert set(release_files) == set(expected)
