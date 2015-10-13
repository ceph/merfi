from mock import call, patch
import pytest
from merfi.backends import gpg
from merfi.tests.backends.base import BaseBackendTest

class TestGpg(BaseBackendTest):

    backend = gpg.Gpg([])

    # args to merfi.backends.gpg.util's run()
    detached = ['gpg', '--batch', '--yes', '--armor', '--detach-sig', '--output', 'Release.gpg', 'Release']
    clearsign = ['gpg', '--batch', '--yes', '--clearsign', '--output', 'InRelease', 'Release']

    @patch("merfi.backends.gpg.util")
    def test_sign_no_files(self, m_util):
        super(TestGpg, self).test_sign_no_files(m_util)
        assert not m_util.run.called

    @patch("merfi.backends.gpg.util")
    def test_sign_two_files(self, m_util, repotree):
        super(TestGpg, self).test_sign_two_files(m_util, repotree)
        # Our repotree fixture has two "Release" files.
        # Each one gets detached-signed and clearsign'd.
        calls = [
            call(self.detached),
            call(self.clearsign),
            call(self.detached),
            call(self.clearsign),
        ]
        m_util.run.assert_has_calls(calls)
