from merfi.collector import RepoCollector
from os.path import join, dirname


class TestRepoCollector(object):

    def setup(self):
        self.paths = RepoCollector(path='/', _eager=False)

    def test_simple_tree(self, deb_repotree):
        paths = RepoCollector(path=deb_repotree)
        # The root of the deb_repotree fixture is itself a repository.
        expected = [ deb_repotree ]
        assert set(paths) == set(expected)

    def test_path_is_absolute(self):
        assert self.paths._abspath('/') == '/'

    def test_path_is_not_absolute(self):
        assert self.paths._abspath('directory').startswith('/')

    def test_debian_release_files(self, deb_repotree):
        paths = RepoCollector(deb_repotree)
        release_files = paths.debian_release_files
        # The root of the deb_repotree fixture is itself a repository.
        expected = [
            join(deb_repotree, 'dists', 'trusty', 'Release'),
            join(deb_repotree, 'dists', 'precise', 'Release'),
        ]
        assert set(release_files) == set(expected)

    def test_debian_nested_release_files(self, nested_deb_repotree):
        # go one level up
        path = dirname(nested_deb_repotree)
        paths = RepoCollector(path)
        release_files = paths.debian_release_files
        expected = [
            join(nested_deb_repotree, 'dists', 'trusty', 'Release'),
            join(nested_deb_repotree, 'dists', 'precise', 'Release'),
        ]
        assert set(release_files) == set(expected)

    def test_rpm_files(self, rpm_repotree):
        paths = RepoCollector(rpm_repotree)
        rpm_files = paths.rpm_files
        # The repotree fixture contains two repositories, one package in each.
        expected = [
            join(rpm_repotree, 'el6', 'test.el6.rpm'),
            join(rpm_repotree, 'el7', 'test.el7.rpm'),
        ]
        assert set(rpm_files) == set(expected)

    def test_repomd_files(self, rpm_repotree):
        paths = RepoCollector(rpm_repotree)
        repomd_files = paths.rpm_repomd_files
        # The repotree fixture contains two repositories.
        expected = [
            join(rpm_repotree, 'el6', 'repodata', 'repomd.xml'),
            join(rpm_repotree, 'el7', 'repodata', 'repomd.xml'),
        ]
        assert set(repomd_files) == set(expected)
