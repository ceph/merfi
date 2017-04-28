from merfi.collector import RepoCollector, DebRepo
from os.path import join


class TestRepoCollector(object):

    def setup(self):
        self.repos = RepoCollector(path='/', _eager=False)

    def test_simple_tree(self, deb_repotree):
        path = join(deb_repotree, 'jewel')
        repos = RepoCollector(path)
        assert [r.path for r in repos] == [path]

    def test_path_is_absolute(self):
        assert self.repos._abspath('/') == '/'

    def test_path_is_not_absolute(self):
        assert self.repos._abspath('directory').startswith('/')

    def test_debian_repo(self, deb_repotree):
        # Select the root of one repository in our fixture.
        path = join(deb_repotree, 'jewel')
        repos = RepoCollector(path)
        assert repos == [DebRepo(path)]

    def test_debian_release_files(self, deb_repotree):
        # Select the root of one repository in our fixture.
        path = join(deb_repotree, 'jewel')
        repos = RepoCollector(path)
        expected = [
            join(path, 'dists', 'trusty', 'Release'),
            join(path, 'dists', 'xenial', 'Release'),
        ]
        assert set(repos[0].releases) == set(expected)

    def test_nested_debian_repo(self, deb_repotree):
        repos = RepoCollector(deb_repotree)
        # Verify that we found the two repos.
        expected = [DebRepo(join(deb_repotree, 'jewel')),
                    DebRepo(join(deb_repotree, 'luminous'))]
        assert repos == expected

    def test_debian_nested_release_files(self, deb_repotree):
        repos = RepoCollector(deb_repotree)
        release_files = [rfile for repo in repos for rfile in repo.releases]
        expected = [
            join(deb_repotree, 'jewel', 'dists', 'trusty', 'Release'),
            join(deb_repotree, 'jewel', 'dists', 'xenial', 'Release'),
            join(deb_repotree, 'luminous', 'dists', 'trusty', 'Release'),
            join(deb_repotree, 'luminous', 'dists', 'xenial', 'Release'),
        ]
        assert set(release_files) == set(expected)
