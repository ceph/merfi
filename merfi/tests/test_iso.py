import os
import pytest
import subprocess
from merfi.iso import Iso
from merfi.util import which

class TestIso(object):

    def create_test_iso(self, output_dir):
        iso = Iso([])
        f = output_dir.join('test.iso')
        f.write('ISOCONTENTS')
        iso.output = str(f)
        iso.make_sha256sum()
        return iso

    def test_sha256sum_contents(self, tmpdir):
        iso = self.create_test_iso(tmpdir)
        with open(iso.output_checksum, 'r') as chsumf:
            assert chsumf.read() == "d8d322f6864229f8c9ef1b0845dd9e182c563c508fec30618fdb9b57c70a0147  test.iso\n"

    # Validate output_checksum's syntax with sha256sum.
    # The reason we shell out to sha256sum here is that it functionally
    # validates what a user would do with this ISO's checksum file: a user
    # would run `sha256sum -c` on it.
    @pytest.mark.skipif(which('sha256sum') is None, reason='sha256sum is not installed')
    def test_sha256sum_command(self, tmpdir):
        iso = self.create_test_iso(tmpdir)
        os.chdir(os.path.dirname(iso.output_checksum))
        assert subprocess.call(['sha256sum', '-c', iso.output_checksum]) == 0
