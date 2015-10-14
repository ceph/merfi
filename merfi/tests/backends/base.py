import pytest
import merfi

# inherit this class when testing a backend
class BaseBackendTest(object):

    def test_sign_no_files(self, m_util, tmpdir):
        self.backend.path = str(tmpdir)
        self.backend.sign()

    def test_sign_two_files(self, m_util, repotree):
        # Use our tempdir fixture.
        self.backend.path = repotree
        # The Gpg backend requires the the 'check' config key to be defined.
        # (Maybe this is something that Tambo always sets, when merfi is run on
        # the cmdline?)
        merfi.config['check'] = False
        self.backend.sign()
