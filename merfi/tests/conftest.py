import os
import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')


@pytest.fixture(scope="function")
def deb_repotree(request):
    """ Return a single Debian repository to sign. """
    return os.path.join(FIXTURES_DIR, 'debrepos', 'nested')


@pytest.fixture(scope="function")
def nested_deb_repotree(request):
    """ Return a single Debian repository to sign. """
    return os.path.join(FIXTURES_DIR, 'debrepos', 'nested')
