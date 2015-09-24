from mock import patch
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
        return super(TestGpg, self).test_sign_no_files(m_util)

    @patch("merfi.backends.gpg.util")
    def test_sign_two_files(self, m_util, repotree):
        return super(TestGpg, self).test_sign_two_files(m_util, repotree)
