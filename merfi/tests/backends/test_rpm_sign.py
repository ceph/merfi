from mock import call, patch
import pytest
from merfi.backends import rpm_sign
from merfi.tests.backends.base import BaseBackendTest
from tambo import Transport

class TestRpmSign(BaseBackendTest):

    backend = rpm_sign.RpmSign([])
    # fake command-line args
    argv = ['merfi', '--key', 'mykey']
    backend.parser = Transport(argv, options=backend.options)
    backend.parser.parse_args()

    # args to merfi.backends.rpm_sign.util's run()
    detached = ['rpm-sign', '--key', 'mykey', '--detachsign', 'Release', '--output', 'Release.gpg']
    # args to merfi.backends.rpm_sign.util's run_output()
    clearsign = ['rpm-sign', '--key', 'mykey', '--clearsign', 'Release']

    @patch('merfi.backends.rpm_sign.util')
    def test_sign_no_files(self, m_util, tmpdir):
        super(TestRpmSign, self).test_sign_no_files(m_util, tmpdir)
        assert not m_util.run.called
        assert not m_util.run_output.called

    @patch('merfi.backends.rpm_sign.util')
    def test_sign_two_files(self, m_util, repotree):
        # Fake the return values for inline-signing
        m_util.run_output.return_value = ('--PGP SIGNED MESSAGE--', None, None)
        super(TestRpmSign, self).test_sign_two_files(m_util, repotree)
        detached_calls = [
            call(self.detached),
            call(self.detached),
        ]
        clearsign_calls = [
            call(self.clearsign),
            call(self.clearsign),
        ]
        m_util.run.assert_has_calls(detached_calls)
        m_util.run_output.assert_has_calls(clearsign_calls)
