import pytest
import merfi
from mock import call

# inherit this class when testing a backend
class BaseBackendTest(object):

    def test_sign_no_files(self, m_util):
        self.backend.path = ''
        self.backend.sign()
        assert not m_util.run.called

    def test_sign_two_files(self, m_util, repotree):
        # Use our tempdir fixture.
        self.backend.path = repotree
        # The Gpg backend requires the the 'check' config key to be defined.
        # (Maybe this is something that Tambo always sets, when merfi is run on
        # the cmdline?)
        merfi.config['check'] = False
        self.backend.sign()
        # Our repotree fixture has two "Release" files.
        # Each one gets detached-signed and clearsign'd.
        calls = [
            call(self.detached),
            call(self.clearsign),
            call(self.detached),
            call(self.clearsign),
        ]
        m_util.run.assert_has_calls(calls)
