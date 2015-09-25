from merfi import base


class TestBase(object):

    def setup(self):
        self.base = base.BaseCommand(None)

    def test_dependency_help_is_installed(self):
        self.base.executable = 'ls'
        assert 'is installed and available' in self.base.dependency_help()

    def test_dependency_help_is_not_installed(self):
        self.base.executable = 'ffffffffffffffffffffff'
        assert 'is not installed or available' in self.base.dependency_help()
