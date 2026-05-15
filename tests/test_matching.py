from autorouting import Router, Route, MatchedRoute


router = Router()

router.add("path/to/{var:digit}", "GET", "component A")
router.add("path/to/{var}", "GET", "component B")
router.add("download/{name:path}", "GET", "component C")
router.add("/path", "GET", "component D")


def test_route_matching():
    assert router.get("path/to/1", "GET") == (
        "path/to/1",
        "GET",
        "component A",
        {"var": "1"}
    )

    assert router.get("path/to/abc", "GET") == (
        "path/to/abc",
        "GET",
        "component B",
        {"var": "abc"}
    )

    assert router.get("download/file", "GET") == (
        "download/file",
        "GET",
        "component C",
        {"name": "file"}
    )


def test_route_matched_value():
    found = router.get("/path", "GET")
    assert isinstance(found, MatchedRoute)
    assert found == ("/path", "GET", "component D", {})
    assert found == MatchedRoute(
        path="/path",
        namespace="GET",
        component="component D",
        params={}
    )


def test_no_match():
    assert router.get("unknown/test", "GET") is None


def test_description():
    assert dict(router) == {
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
        '/path': {
            'GET': [
                Route(
                    component='component D',
                    requirements={},
                    priority=0
                )
            ]
        }
    }
