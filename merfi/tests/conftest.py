import os
import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')


@pytest.fixture(scope="function")
def deb_repotree(request):
    """ Return a directory of Debian repositories to sign. """
    return os.path.join(FIXTURES_DIR, 'debrepos')
