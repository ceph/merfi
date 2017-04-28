from merfi.collector import RepoCollector, DebRepo
from os.path import join, dirname


class TestRepoCollector(object):

    def setup(self):
        self.repos = RepoCollector(path='/', _eager=False)

    def test_simple_tree(self, deb_repotree):
        repos = RepoCollector(path=deb_repotree)
        # The root of the deb_repotree fixture is itself a repository.
        assert [r.path for r in repos] == [deb_repotree]

    def test_path_is_absolute(self):
        assert self.repos._abspath('/') == '/'

    def test_path_is_not_absolute(self):
        assert self.repos._abspath('directory').startswith('/')

    def test_debian_repo(self, deb_repotree):
        repos = RepoCollector(deb_repotree)
        # The root of the deb_repotree fixture is itself a repository.
        assert repos == [DebRepo(deb_repotree)]

    def test_debian_release_files(self, deb_repotree):
        repos = RepoCollector(deb_repotree)
        # The root of the deb_repotree fixture is itself a repository.
        expected = [
            join(deb_repotree, 'dists', 'trusty', 'Release'),
            join(deb_repotree, 'dists', 'xenial', 'Release'),
        ]
        assert set(repos[0].releases) == set(expected)

    def test_nested_debian_repo(self, deb_repotree):
        # go one level up
        path = dirname(deb_repotree)
        repos = RepoCollector(path)
        # Verify that we found the two repo trees.
        expected = [DebRepo(join(path, 'jewel')),
                    DebRepo(join(path, 'luminous'))]
        assert repos == expected

    def test_debian_nested_release_files(self, deb_repotree):
        # go one level up
        path = dirname(deb_repotree)
        repos = RepoCollector(path)
        release_files = [rfile for repo in repos for rfile in repo.releases]
        expected = [
            join(path, 'jewel', 'dists', 'trusty', 'Release'),
            join(path, 'jewel', 'dists', 'xenial', 'Release'),
            join(path, 'luminous', 'dists', 'trusty', 'Release'),
            join(path, 'luminous', 'dists', 'xenial', 'Release'),
        ]
        assert set(release_files) == set(expected)
