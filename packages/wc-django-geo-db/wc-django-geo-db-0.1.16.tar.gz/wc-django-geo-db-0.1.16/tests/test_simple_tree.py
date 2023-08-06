import pytest
from pprint import pprint

from wcd_geo_db.modules.bank.db import Division

from .fixtures import *


@pytest.mark.django_db
def test_tree_descendants(simple_tree_data):
    descendants = list(Division.objects.filter(id=1).descendants())
    assert len(descendants) == 2

    descendants = list(Division.objects.filter(id=1).descendants())
    assert len(descendants) == 2

    descendants = list(Division.objects.filter(id=2).descendants())
    assert len(descendants) == 1

    descendants = list(Division.objects.filter(id=2).descendants())
    assert len(descendants) == 1

    descendants = list(Division.objects.filter(id=10).descendants())
    assert len(descendants) == 1

    descendants = list(Division.objects.filter(id=8).descendants())
    assert len(descendants) == 0


@pytest.mark.django_db
def test_tree_ancestors(simple_tree_data):
    ancestors = list(Division.objects.ancestors())
    assert len(ancestors) == 3

    ancestors = list(Division.objects.filter(id=10).ancestors())
    assert len(ancestors) == 1

    ancestors = list(Division.objects.filter(id=2).ancestors())
    assert len(ancestors) == 2


@pytest.mark.django_db
def test_tree_roots(simple_tree_data):
    roots = list(Division.objects.roots())
    assert len(roots) == 2

    roots = list(Division.objects.filter(id=10).roots())
    assert len(roots) == 1

    roots = list(Division.objects.filter(id=2).roots())
    assert len(roots) == 1


@pytest.mark.django_db
def test_tree_validity(simple_invalid_tree_data):
    valid = list(Division.objects.roughly_valid_elements())
    assert len(valid) == 4

    updated = Division.objects.update_roughly_invalid_tree()
    assert updated == 10

    invalid = list(Division.objects.roughly_valid_elements(validity=False).values_list('id', 'path'))
    assert len(invalid) == 0

    # tree = list(Division.objects.order_by('parent__path__depth', 'path__depth').values_list('path', 'id', 'parent__path'))
    # pprint(tree)
