import re
import pytest
from autorouting import Router, MatchedRoute
from autorouting.url import RouteURL
from hamcrest import equal_to


def test_route_naming():
    router = Router()
    router.add("path/to/{var:digit}", "Component", "component A", name="A")

    with pytest.raises(NotImplementedError):
        router.get_by_name('A')

    router.finalize()
    url = router.get_by_name('A')
    assert url == RouteURL(
        url='path/to/{var}',
        slugs={'var': ('digit', re.compile('^\\d+$'))}
    )


def test_route_naming_duplicate_different_group():
    router = Router()
    router.add("path/to/{var:digit}", "Component", "component A", name="A")

    with pytest.raises(NameError) as exc:
        router.add("path/to/A", "Component", "component A", name="A")

    assert str(exc.value) == "Name 'A' is already in use."


def test_route_naming_duplicate_same_group():
    router = Router()
    router.add(
        "path/to/{var:digit}", "Component", "component A",
        name="A", requirements={'user': equal_to('admin')}, priority=1)
    router.add(
        "path/to/{var:digit}", "Component", "component B", name="A")

    router.finalize()
    url = router.get_by_name('A')
    assert url == RouteURL(
        url='path/to/{var}',
        slugs={'var': ('digit', re.compile('^\\d+$'))}
    )

    found = router.get("path/to/1", "Component")
    assert found == MatchedRoute(
        path='path/to/1',
        namespace='Component',
        component='component B',
        params={'var': '1'}
    )

    found = router.get("path/to/1", "Component", extra={"user": "admin"})
    assert found == MatchedRoute(
        path='path/to/1',
        namespace='Component',
        component='component A',
        params={'var': '1'}
    )
