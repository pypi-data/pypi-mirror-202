import pytest

from wcd_geo_db.client import GeoClient
from wcd_geo_db.conf import Settings
from wcd_geo_db.modules.bank.dtos import ExtendedDivisionDTO
from django.contrib.gis.geos import Point
from wcd_geo_db.modules.code_seeker import registry

from .fixtures import *


@pytest.mark.django_db
def test_extended_resolver(full_locality_path):
    client = GeoClient(
        settings=Settings(),
        code_seeker_registry=registry,
    )
    divisions_client = client.bank.divisions
    division, *_ = divisions_client.get(ids=(5,), as_dto=ExtendedDivisionDTO)

    assert len(_) == 0
    assert division.path == [1, 2, 3, 4, 5]

    p1 = division.geometry.location
    p2 = Point(30.3926089, 50.4021702)
    assert (p1.x, p1.y) == (p2.x, p2.y)

    division, *_ = divisions_client.get(ids=(5,))
    assert not hasattr(division, 'geometry')
