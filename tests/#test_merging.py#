from autorouting import Router, Route, MatchedRoute


def test_union():
    router1 = Router()
    router2 = Router()

    router1.add("path/to/{var:digit}", "GET", "component A")
    router1.add("download/{name:path}", "GET", "component C")

    router2.add("path/to/{var}", "GET", "component B")
    router2.add("/path", "GET", "component D")

    router3 = router1 | router2
    assert dict(router3) == {
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


def test_inplace_union():
    router1 = Router()
    router2 = Router()

    router1.add("path/to/{var:digit}", "GET", "component A")
    router1.add("download/{name:path}", "GET", "component C")

    router2.add("path/to/{var}", "GET", "component B")
    router2.add("/path", "GET", "component D")

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
