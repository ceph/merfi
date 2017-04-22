import os
import pytest
import shutil

# TODO: Enhance this fixture so that we distinguish between the "Release"
# files that need to be signed and the ones that do not.
#   - Create more bogus "Releases" files that don't need to be signed.
#   - Write a line "SHA256:" into the correct "Releases" file that *should* be
#     signed.
# See https://github.com/alfredodeza/merfi/issues/6
@pytest.fixture(scope="function")
def deb_repotree(request, tmpdir):
    # Create a basic skeleton repository with "Release" files to sign.
    top_dir = str(tmpdir)
    # Top directories:
    os.mkdir(os.path.join(top_dir, 'db'))
    os.mkdir(os.path.join(top_dir, 'dists'))
    os.mkdir(os.path.join(top_dir, 'pool'))
    # Distro "Release" files:
    for distro in ['trusty', 'xenial']:
        distro_dir = os.path.join(top_dir, 'dists', distro)
        os.mkdir(distro_dir)
        release_file = open(os.path.join(distro_dir, 'Release'), 'w')
        release_file.write('some Release metadata for %s' % distro)
        release_file.close()

    return top_dir


@pytest.fixture(scope="function")
def nested_deb_repotree(request, tmpdir):
    # Create a basic skeleton repository with "Release" files to sign.
    directory = str(tmpdir)
    os.makedirs(os.path.join(directory, 'nested'))
    top_dir = os.path.join(directory, 'nested')
    # Top directories:
    os.mkdir(os.path.join(top_dir, 'db'))
    os.mkdir(os.path.join(top_dir, 'dists'))
    os.mkdir(os.path.join(top_dir, 'pool'))
    # Distro "Release" files:
    for distro in ['trusty', 'xenial']:
        distro_dir = os.path.join(top_dir, 'dists', distro)
        os.mkdir(distro_dir)
        release_file = open(os.path.join(distro_dir, 'Release'), 'w')
        release_file.write('some Release metadata for %s' % distro)
        release_file.close()

    return top_dir

@pytest.fixture(scope="function")
def rpm_repotree(request, tmpdir):
    """ Create a basic set of repositories with .rpm files to sign. """
    top_dir = str(tmpdir)
    # RPM files and repo metadata:
    for distro in ['el6', 'el7']:
        distro_dir = os.path.join(top_dir, distro)
        os.mkdir(distro_dir)
        # Dummy .rpm file:
        rpm_filename = 'test.%s.rpm' % distro
        rpm_file = open(os.path.join(distro_dir, rpm_filename), 'w')
        rpm_file.write('some RPM content for %s' % distro)
        rpm_file.close()
        # Dummy Yum/DNF repository metadata:
        os.mkdir(os.path.join(distro_dir, 'repodata'))
        repomd_path = os.path.join(distro_dir, 'repodata', 'repomd.xml')
        repomd_file = open(repomd_path, 'w')
        repomd_file.write('<xml>some Yum/DNF data for %s</xml>' % distro)
        repomd_file.close()

    return top_dir
