import pytest

from aioresponses import aioresponses

from quickbuild import QBClient


@pytest.fixture
def aiohttp_mock():
    with aioresponses() as mock:
        yield mock


@pytest.fixture
def client():
    yield QBClient('http://server')
