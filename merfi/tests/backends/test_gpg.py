from merfi.backends import gpg


class TestGpgGetPath(object):

    def setup(self):
        self.gpg_ = gpg.Gpg(None)

    def test_no_last_argument(self):
        args = ['gpg', '--output', 'signed']
        result = self.gpg_.get_path(args)
        assert result.startswith('/')
        assert result.endswith('signed') is False

    def test_last_argument(self):
        args = ['gpg', '--output', 'signed', '/']
        result = self.gpg_.get_path(args)
        assert result == '/'

    def test_no_arguments(self):
        # the parser engine pops the current command so we can
        # certainly end up with an empty argv list
        result = self.gpg_.get_path([])
        assert result.startswith('/')
