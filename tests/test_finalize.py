import pytest
from autorouting import Router, ImmutabilityError


def test_add_finalized():
    router = Router()
    router.finalize()

    with pytest.raises(ImmutabilityError):
        router.add("path/to/{var:digit}", "GET", "component A")


def test_inplace_union_finalized():
    router1 = Router()
    router2 = Router()
    router2.finalize()

    with pytest.raises(ImmutabilityError):
        router2 |= router1
