import fnmatch
from autorouting import Router
from autorouting.matchers import Wildcard
from hamcrest.core.core.isequal import IsEqual



router = Router()

router.add("path/to/{var}", 'GET', 'component A',
           requirements={'name': Wildcard('f??')})

router.add("path/to/{var}", 'GET', 'component B',
           requirements={
               'name': Wildcard('f*'),
               'user': IsEqual('admin')
           })

router.add("path/to/{var}", 'GET', 'component C')

router.finalize()




def test_matching():
    found = list(
        router.match(
            'path/to/1', 'GET', extra={"name": "fee", "user": "admin"}
        )
    )
    assert found == [
        ('path/to/1', 'GET', 'component B', {'var': '1'}),
        ('path/to/1', 'GET', 'component A', {'var': '1'}),
        ('path/to/1', 'GET', 'component C', {'var': '1'})
    ]

    found = list(
        router.match(
            'path/to/1', 'GET', extra={"name": "forrest", "user": "admin"}
        )
    )
    assert found == [
        ('path/to/1', 'GET', 'component B', {'var': '1'}),
        ('path/to/1', 'GET', 'component C', {'var': '1'})
    ]

    found = list(
        router.match(
            'path/to/1', 'GET', extra={"name": "forrest", "user": "john"}
        )
    )
    assert found == [
        ('path/to/1', 'GET', 'component C', {'var': '1'})
    ]
