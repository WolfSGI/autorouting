import re
import pytest
from autorouting.url import extract_slugs, RouteURL


def test_slug_extractor():
    slugs = extract_slugs('/test')
    assert slugs == {}

    slugs = extract_slugs('/test{bit}')
    assert slugs == {
        'bit': (
            'string',
            re.compile('^[^/]+$'),
        ),
    }

def test_slug_extractor_duplicate():
    with pytest.raises(NameError) as exc:
        extract_slugs('/test{bit}/{bit}')

    assert str(exc.value) == "Duplicate variable name in url: bit."


def test_route_url_from_path():
    route = RouteURL.from_path("/test")
    assert route == RouteURL(url='/test', slugs=None)

    route = RouteURL.from_path("/user/{uid}")
    assert route == RouteURL(
        url='/user/{uid}',
        slugs={
            'uid': ('string', re.compile('^[^/]+$'))
        }
    )

    route = RouteURL.from_path("/user/{uid:digit}")
    assert route == RouteURL(
        url='/user/{uid}',
        slugs={
            'uid': ('digit', re.compile('^\\d+$'))
        }
    )

    route = RouteURL.from_path("/user/{uid:^[john|robert]$}")
    assert route == RouteURL(
        url='/user/{uid}',
        slugs={
            'uid': ('regexp', re.compile('^^[john|robert]$$'))
        }
    )


def test_route_url_match():
    route = RouteURL(
        url='/user/{uid}',
        slugs={
            'uid': ('digit', re.compile('^\\d+$'))
        }
    )

    matched, unmatched = route.match(uid="1")
    assert matched == {
        'uid': '1',
    }
    assert unmatched == {}

    with pytest.raises(KeyError) as exc:
        route.match()

    assert str(exc.value) == "'Missing URL variable: uid.'"


def test_route_url_match_regexp():
    route = RouteURL.from_path("/user/{uid:(john|robert)}")
    matched, unmatched = route.match(uid="john")
    assert matched == {"uid": "john"}
    assert unmatched == {}

    matched, unmatched = route.match(uid="robert")
    assert matched == {"uid": "robert"}
    assert unmatched == {}

    with pytest.raises(ValueError) as exc:
        route.match(uid="simon")

    assert str(exc.value) == (
        "'uid' param does not match pattern re.compile('^(john|robert)$')."
    )


def test_route_url_resolve():
    route = RouteURL(
        url='/user/{uid}',
        slugs={
            'uid': ('digit', re.compile('^\\d+$'))
        }
    )

    path, unmatched = route.resolve({"uid": "1"})
    assert path == "/user/1"
    assert unmatched == {}

    path, unmatched = route.resolve({"uid": "1", "page": "2"})
    assert path == "/user/1?page=2"
    assert unmatched == {}

    path, unmatched = route.resolve({"uid": "1", "page": "2"}, qstring=False)
    assert path == "/user/1"
    assert unmatched == {"page": "2"}
