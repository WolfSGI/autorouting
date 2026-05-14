import pytest
from autorouting import Router, Route


class HTTPRouter(Router):

    allowed_namespaces = (
        "GET", "HEAD", "PUT", "DELETE", "PATCH", "POST", "OPTIONS"
    )


def test_namespace_unknown():
    router = HTTPRouter()

    with pytest.raises(ValueError) as exc:
        router.add("/not_http", "WHATEVER", "component D")

    assert str(exc.value) == (
        "Unknown namespace: WHATEVER. Expected one of "
        "('GET', 'HEAD', 'PUT', 'DELETE', 'PATCH', 'POST', 'OPTIONS')"
    )


def test_namespace_diverging_union():
    router1 = HTTPRouter()
    router2 = Router()

    router1.add("path/to/{var:digit}", "GET", "component A")
    router1.add("download/{name:path}", "GET", "component C")

    router2.add("path/to/{var}", "GET", "component B")
    router2.add("/not_http", "WHATEVER", "component D")

    with pytest.raises(ValueError):
        router1 | router2


def test_inplace_diverging_union():
    router1 = Router()
    router2 = Router()

    router1.add("path/to/{var:digit}", "GET", "component A")
    router1.add("download/{name:path}", "GET", "component C")

    router2.add("path/to/{var}", "GET", "component B")
    router2.add("/not_http", "WHATEVER", "component D")

    router2 |= router1
    assert dict(router2) == {
        'path/to/{var:digit}': {
            'GET': [
                Route(
                    component='component A',
                    requirements={},
                    priority=0
                )
            ]
        },
        'path/to/{var}': {
            'GET': [
                Route(
                    component='component B',
                    requirements={},
                    priority=0
                )
            ]
        },
        'download/{name:path}': {
            'GET': [
                Route(
                    component='component C',
                    requirements={},
                    priority=0
                )
            ]
        },
        '/not_http': {
            'WHATEVER': [
                Route(
                    component='component D',
                    requirements={},
                    priority=0
                )
            ]
        }
    }
