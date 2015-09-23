from pytest import raises
from merfi import util


class TestGetPath(object):

    def test_no_last_argument(self):
        args = ['gpg', '--output', 'signed']
        with raises(RuntimeError) as error:
            util.infer_path(args)
        assert 'is not a valid path' in str(error.value)

    def test_last_argument(self):
        args = ['gpg', '--output', 'signed', '/']
        result = util.infer_path(args)
        assert result == '/'

    def test_no_arguments(self):
        # the parser engine pops the current command so we can
        # certainly end up with an empty argv list
        result = util.infer_path([])
        assert result.startswith('/')
