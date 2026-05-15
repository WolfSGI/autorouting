import pytest
from autorouting import Router, Route, MatchedRoute


def test_no_priority():
    router = Router()
    router.add('/whatever', 'GET', 'Component 1')
    router.add('/whatever', 'GET', 'Component 2')

    route = router.get("/whatever", "GET")
    assert route == MatchedRoute(
        path='/whatever',
        namespace='GET',
        component='Component 1',
        params={}
    )

    routes = list(router.match("/whatever", "GET"))
    assert routes == [
       MatchedRoute(
           path='/whatever',
           namespace='GET',
           component='Component 1',
           params={}
       ),
        MatchedRoute(
           path='/whatever',
            namespace='GET',
            component='Component 2',
            params={}
        ),
    ]


def test_priority():
    router = Router()
    router.add('/whatever', 'GET', 'Component 1')
    router.add('/whatever', 'GET', 'Component 2', priority=1)
    router.add('/whatever', 'GET', 'Component 3')

    route = router.get("/whatever", "GET")
    assert route == MatchedRoute(
        path='/whatever',
        namespace='GET',
        component='Component 2',
        params={}
    )

    routes = list(router.match("/whatever", "GET"))
    assert routes == [
        MatchedRoute(
            path='/whatever',
            namespace='GET',
            component='Component 2',
            params={}
        ),
        MatchedRoute(
            path='/whatever',
            namespace='GET',
            component='Component 1',
            params={}
        ),
        MatchedRoute(
           path='/whatever',
            namespace='GET',
            component='Component 3',
            params={}
        ),
    ]


def test_competing_priority():
    router = Router()
    router.add('/whatever', 'GET', 'Component 1', priority=2)
    router.add('/whatever', 'GET', 'Component 2', priority=1)
    router.add('/whatever', 'GET', 'Component 3', priority=99)

    route = router.get("/whatever", "GET")
    assert route == MatchedRoute(
        path='/whatever',
        namespace='GET',
        component='Component 3',
        params={}
    )

    routes = list(router.match("/whatever", "GET"))
    assert routes == [
        MatchedRoute(
            path='/whatever',
            namespace='GET',
            component='Component 3',
            params={}
        ),
        MatchedRoute(
            path='/whatever',
            namespace='GET',
            component='Component 1',
            params={}
        ),
        MatchedRoute(
           path='/whatever',
            namespace='GET',
            component='Component 2',
            params={}
        ),
    ]
