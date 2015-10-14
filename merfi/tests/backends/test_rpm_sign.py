from merfi.backends import rpm_sign
from merfi.tests.util import CallRecorder
from tambo import Transport


class RpmSign(object):

    def setup(self):
        self.backend = rpm_sign.RpmSign([])
        self.backend.detached = CallRecorder()
        self.backend.clear_sign = CallRecorder()
        # fake command-line args
        self.argv = ['merfi', '--key', 'mykey']
        self.backend.parser = Transport(
            self.argv, options=self.backend.options
        )
        self.backend.parser.parse_args()

        # args to merfi.backends.rpm_sign.util's run()
        self.detached = [
            'rpm-sign', '--key', 'mykey', '--detachsign',
            'Release', '--output', 'Release.gpg']
        # args to merfi.backends.rpm_sign.util's run_output()
        self.clearsign = [
            'rpm-sign', '--key', 'mykey',
            '--clearsign', 'Release']

    def sign(self, directory):
        self.backend.path = directory
        self.backend.sign()


class TestRpmSign(RpmSign):

    def test_sign_no_files(self, tmpdir):
        self.sign(str(tmpdir))
        assert self.backend.detached.calls == []
        assert self.backend.clear_sign.calls == []

    def test_sign_two_files_detached_and_clearsign(self, repotree):
        self.sign(repotree)
        assert len(self.backend.detached.calls) == 2
        assert len(self.backend.clear_sign.calls) == 2

    def test_sign_two_files_detached_args(self, repotree):
        self.sign(repotree)
        assert self.backend.detached.calls[0][0][0] == self.detached
        assert self.backend.detached.calls[1][0][0] == self.detached

    def test_sign_two_files_clear_sign_args(self, repotree):
        self.sign(repotree)
        # first call, second argument (the command to run)
        assert self.backend.clear_sign.calls[0][0][1] == self.clearsign
        # second call, second argument (the command to run)
        assert self.backend.clear_sign.calls[1][0][1] == self.clearsign
