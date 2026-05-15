from autorouting.matchers import Wildcard, Matcher


def test_matcher_wildcard_type():
    matcher = Wildcard("whatever")
    assert isinstance(matcher, str) is True


def test_matcher_wildcard_empty():
    matcher = Wildcard()
    assert matcher.matches('toto') is False
    assert matcher.matches('') is True


def test_matcher_wildcard_matching():
    matcher = Wildcard("f??")
    assert matcher.matches('foo') is True
    assert matcher.matches('foot') is False

    matcher = Wildcard("f*")
    assert matcher.matches('foo') is True
    assert matcher.matches('foot') is True
    assert matcher.matches('') is False
    assert matcher.matches('a') is False

    matcher = Wildcard("*")
    assert matcher.matches('foo') is True
    assert matcher.matches('bar') is True
    assert matcher.matches('') is True
