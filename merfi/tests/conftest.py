import os
import pytest
import shutil
import tempfile

@pytest.fixture(scope="module")
def repotree(request):
    # Create a basic skeleton repository with "Release" files to sign.
    top_dir = tempfile.mkdtemp(suffix='.merfi')
    # Top directories:
    os.mkdir(os.path.join(top_dir, 'db'))
    os.mkdir(os.path.join(top_dir, 'dists'))
    os.mkdir(os.path.join(top_dir, 'pool'))
    # Distro "Release" files:
    for distro in ['precise', 'trusty']:
        distro_dir = os.path.join(top_dir, 'dists', distro)
        os.mkdir(distro_dir)
        release_file = open(os.path.join(distro_dir, 'Release'), 'w')
        release_file.write('some Release metadata for %s' % distro)
        release_file.close()

    def fin():
        shutil.rmtree(top_dir)
    request.addfinalizer(fin)
    return top_dir
