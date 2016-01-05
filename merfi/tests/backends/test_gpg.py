from mock import call, patch
import pytest
from merfi.backends import gpg

class TestGpg(object):

    backend = gpg.Gpg([])

    # args to merfi.backends.gpg.util's run()
    detached = ['gpg', '--batch', '--yes', '--armor', '--detach-sig', '--output', 'Release.gpg', 'Release']
    clearsign = ['gpg', '--batch', '--yes', '--clearsign', '--output', 'InRelease', 'Release']

    @patch("merfi.backends.gpg.util")
    def test_sign_no_files(self, m_util, tmpdir):
        self.backend.path = str(tmpdir)
        self.backend.sign()
        assert not m_util.run.called

    @patch("merfi.backends.gpg.util")
    def test_sign_two_files(self, m_util, deb_repotree):
        self.backend.path = deb_repotree
        self.backend.sign()
        # Our deb_repotree fixture has two "Release" files.
        # Each one gets detached-signed and clearsign'd.
        calls = [
            call(self.detached),
            call(self.clearsign),
            call(self.detached),
            call(self.clearsign),
        ]
        m_util.run.assert_has_calls(calls)
