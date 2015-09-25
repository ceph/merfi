from pytest import raises
from merfi import util


class TestInferPath(object):

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


class TestDependencyCheck(object):

    def test_silent_does_not_raise(self):
        result = util.check_dependency('ls', silent=True)
        assert result is None

    def test_silent_does_not_output(self, capsys):
        util.check_dependency('ls', silent=True)
        out, err = capsys.readouterr()
        assert out == ''
        assert err == ''

    def test_not_silent_prints_when_erroring(self, capsys):
        with raises(RuntimeError):
            util.check_dependency('ffffffffffffff')
        out, err = capsys.readouterr()
        assert 'could not find' in out
