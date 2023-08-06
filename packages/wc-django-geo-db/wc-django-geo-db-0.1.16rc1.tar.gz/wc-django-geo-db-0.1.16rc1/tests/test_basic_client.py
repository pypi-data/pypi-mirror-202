import pytest

from wcd_geo_db.client import GeoClient
from wcd_geo_db.conf import Settings
from wcd_geo_db.modules.code_seeker import registry, ISO3166_SEEKER
from wcd_geo_db.modules.bank.db import Division, DivisionCode

from .fixtures import *


@pytest.mark.django_db
def test_simple_divisions_client_lookups(simple_tree_data):
    client = GeoClient(
        settings=Settings(),
        code_seeker_registry=registry,
    )
    divisions_client = client.bank.divisions
    divisions = divisions_client.get(ids=(1,))

    assert len(divisions) == 1
    assert divisions[0].path == [1]

    divisions = divisions_client.find(
        levels=(DivisionLevel.ADMINISTRATIVE_LEVEL_1,)
    )

    assert len(divisions) == 1
    assert divisions[0] == 2

    divisions = divisions_client.find(
        levels=(DivisionLevel.COUNTRY,)
    )

    assert len(divisions) == 2
    assert 1 in divisions
    assert 10 in divisions

    divisions = divisions_client.find_descendants(
        ids=[1],
        levels=(DivisionLevel.ADMINISTRATIVE_LEVEL_2,)
    )

    assert len(divisions) == 0

    divisions = divisions_client.find_descendants(
        ids=[1],
        levels=(DivisionLevel.ADMINISTRATIVE_LEVEL_1,)
    )

    assert len(divisions) == 1
    assert divisions[0] == 2


@pytest.mark.django_db
def test_simple_divisions_codes_lookup(simple_tree_data):
    client = GeoClient(
        settings=Settings(),
        code_seeker_registry=registry,
    )
    divisions_client = client.bank.divisions
    divisions = divisions_client.get_by_code(ISO3166_SEEKER.name, 'UNKNO')

    assert len(divisions) == 1
    assert divisions[0].path == [10]

    divisions = divisions_client.get_by_code(ISO3166_SEEKER.name, 'UNKN')

    assert len(divisions) == 1
    assert divisions[0].path == [1, 2]

    divisions = divisions_client.get_by_code(ISO3166_SEEKER.name, 'KNO')

    assert len(divisions) == 1
    assert divisions[0].path == [1]


@pytest.mark.django_db
def test_divisions_simple_search_lookup(simple_divisions_search_data):
    client = GeoClient(
        settings=Settings(),
        code_seeker_registry=registry,
    )
    divisions_client = client.bank.divisions
    d = simple_divisions_search_data
    divisions = divisions_client.find(search_query={'query': 'First'})
    divisions = list(divisions)

    assert len(divisions) == 5
    assert d['first'].id in divisions
    assert d['first_synonyms'].id in divisions
    assert d['first_like'].id in divisions
    assert d['first_like_phrase'].id in divisions
    assert divisions == [
        d['first_synonyms'].id,
        d['first'].id,
        d['first_like_phrase'].id,
        d['first_like'].id,
        d['first_like_fist'].id,
    ]

    divisions = divisions_client.find(search_query={'query': 'like first'})
    divisions = list(divisions)

    assert len(divisions) == 5
    assert d['first_like'].id in divisions
    assert d['first_like_phrase'].id in divisions
    assert divisions == [
        d['first_synonyms'].id,
        d['first_like_phrase'].id,
        d['first_like'].id,
        d['first'].id,
        d['first_like_fist'].id,
    ]

    divisions = divisions_client.find(search_query={'query': 'one'})
    divisions = list(divisions)

    assert len(divisions) == 3
    assert d['first_like'].id in divisions
    assert d['first_like_phrase'].id in divisions
    assert d['second'].id in divisions
