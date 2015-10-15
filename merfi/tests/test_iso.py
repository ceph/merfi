import os
import pytest
import subprocess
from merfi.iso import Iso
from merfi.util import which

class TestIso(object):

    def create_fake_iso(self, output_dir):
        """ Create a fake ISO file, without genisoimage """
        iso = Iso([])
        f = output_dir.join('test.iso')
        f.write('ISOCONTENTS')
        iso.output = str(f)
        iso.make_sha256sum()
        return iso

    def create_real_iso(self, output_dir):
        """ Create a "real" ISO file, using make_iso() (ie genisoimage) """
        # simple contents
        compose_dir = output_dir.mkdir('my-test-contents')
        f = compose_dir.join('contents.txt')
        f.write('This text file will be on our ISO')

        iso = Iso([])
        argv = ['merfi', str(output_dir.join('my-test-contents'))]
        iso.parse_args(argv)
        iso.make_iso()
        iso.make_sha256sum()
        return iso

    def test_sha256sum_contents(self, tmpdir):
        iso = self.create_fake_iso(tmpdir)
        with open(iso.output_checksum, 'r') as chsumf:
            assert chsumf.read() == "d8d322f6864229f8c9ef1b0845dd9e182c563c508fec30618fdb9b57c70a0147  test.iso\n"

    # Validate output_checksum's syntax with sha256sum.
    # The reason we shell out to sha256sum here is that it functionally
    # validates what a user would do with this ISO's checksum file: a user
    # would run `sha256sum -c` on it.
    @pytest.mark.skipif(which('sha256sum') is None, reason='sha256sum is not installed')
    def test_sha256sum_command(self, tmpdir):
        iso = self.create_fake_iso(tmpdir)
        os.chdir(os.path.dirname(iso.output_checksum))
        assert subprocess.call(['sha256sum', '-c', iso.output_checksum]) == 0

    @pytest.mark.skipif(which('genisoimage') is None, reason='genisoimage is not installed')
    def test_make_iso(self, tmpdir):
        iso = self.create_real_iso(tmpdir)
        assert os.path.isfile(str(tmpdir.join('my-test-contents-dvd.iso')))
