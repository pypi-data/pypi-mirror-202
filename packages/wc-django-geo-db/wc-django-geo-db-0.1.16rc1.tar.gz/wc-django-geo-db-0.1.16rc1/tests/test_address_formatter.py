import pytest

from wcd_geo_db.client import GeoClient
from wcd_geo_db.conf import Settings
from wcd_geo_db.modules.code_seeker import registry

from .fixtures import *


@pytest.mark.django_db
def test_address_formatter(simple_tree_data):
    client = GeoClient(
        settings=Settings(),
        code_seeker_registry=registry,
    )
    formatter_client = client.addresses.formatter

    address, = formatter_client.format_addresses(({'divisions_path': [1,2]},), 'ru')
    assert address.id == '2'
    assert len(address.divisions) == 2
    assert address.formatted_address == 'Division 1, Country'

    divisions = client.bank.divisions.get(ids=(1,2))
    divisions = divisions if divisions[0].id == 1 else [divisions[1], divisions[0]]
    address, = formatter_client.format_addresses(({'divisions_path': divisions},), 'ru')
    assert address.id == '2'
    assert len(address.divisions) == 2
    assert address.formatted_address == 'Division 1, Country'

    address, = formatter_client.format_addresses(({'divisions_path': [1]},), 'ru')
    assert address.id == '1'
    assert len(address.divisions) == 1
    assert address.formatted_address == 'Country'

    address, = formatter_client.format_addresses(({'divisions_path': [10]},), 'ru')
    assert address.id == '10'
    assert len(address.divisions) == 1
    assert address.formatted_address == 'Country 2'

    # address, = formatter_client.format_addresses(({'division': 10},), 'ru')
    # assert address.id == '10'
    # assert len(address.divisions) == 1
    # assert address.formatted_address == 'Country 2'


@pytest.mark.django_db
def test_address_formatter_translations(simple_tree_data, django_assert_num_queries):
    client = GeoClient(
        settings=Settings(),
        code_seeker_registry=registry,
    )
    formatter_client = client.addresses.formatter

    divisions = client.bank.divisions.get(ids=(1,2))
    divisions = divisions if divisions[0].id == 1 else [divisions[1], divisions[0]]

    with django_assert_num_queries(4):
        address, = formatter_client.format_addresses(({'divisions_path': (divisions[0], 2)},), 'ru')
        assert address.id == '2'
        assert len(address.divisions) == 2
        assert address.formatted_address == 'Division 1, Country'

    with django_assert_num_queries(3):
        address, = formatter_client.format_addresses(({'divisions_path': (divisions[0], 2)},), 'en')
        assert address.id == '2'
        assert len(address.divisions) == 2
        assert address.formatted_address == 'Division 1[en], Country[en]'

    with django_assert_num_queries(4):
        address, = formatter_client.format_addresses(({'divisions_path': (divisions[0], 2)},), 'ja')
        assert address.id == '2'
        assert len(address.divisions) == 2
        assert address.formatted_address == 'Division 1[ja], Country'

    with django_assert_num_queries(4):
        address, = formatter_client.format_addresses(({'divisions_path': (divisions[0], 2)},), 'uk')
        assert address.id == '2'
        assert len(address.divisions) == 2
        assert address.formatted_address == 'Division 1, Country[uk]'

    with django_assert_num_queries(3):
        address, = formatter_client.format_addresses(({'divisions_path': (divisions[0], 2)},), 'uk', ['en'])
        assert address.id == '2'
        assert len(address.divisions) == 2
        assert address.formatted_address == 'Division 1[en], Country[uk]'


@pytest.mark.django_db
def test_address_formatter_with_names(full_locality_path, django_assert_num_queries):
    client = GeoClient(
        settings=Settings(),
        code_seeker_registry=registry,
    )
    formatter_client = client.addresses.formatter

    division, *_ = client.bank.divisions.get(ids=(5,))

    with django_assert_num_queries(4):
        address, = formatter_client.format_addresses(({'divisions_path': division.path},), 'ru')
        assert address.id == '5'
        assert len(address.divisions) == 5
        assert address.formatted_address == (
            'c. City'
            ', Division 3'
            ', Division 2'
            ', reg. Division 1'
            ', Country'
        )

    with django_assert_num_queries(3):
        address, = formatter_client.format_addresses(({'divisions_path': division.path},), 'en')
        assert address.id == '5'
        assert len(address.divisions) == 5
        assert address.formatted_address == (
            'c[en]. City[en]'
            ', Division 3[en]'
            ', Division 2[en]'
            ', reg[en]. Division 1[en]'
            ', Country[en]'
        )

    with django_assert_num_queries(4):
        address, = formatter_client.format_addresses(({'divisions_path': division.path},), 'ja')
        assert address.id == '5'
        assert len(address.divisions) == 5
        assert address.formatted_address == (
            'c[ja]. City[ja]'
            ', Division 3[ja]'
            ', Division 2[ja]'
            ', reg. Division 1[ja]'
            ', Country'
        )
