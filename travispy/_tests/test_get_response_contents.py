from requests.models import Response
from travispy._helpers import get_response_contents
from travispy.errors import TravisError
import pytest
import textwrap


def test_get_response_contents():
    response = Response()
    response.status_code = 111
    response._content = b'foo'
    with pytest.raises(TravisError) as exception_info:
        get_response_contents(response)
    assert str(exception_info.value) == '[111] foo'

    response._content = ''
    with pytest.raises(TravisError) as exception_info:
        get_response_contents(response)
    assert str(exception_info.value) == textwrap.dedent('''
        [111] Unexpected error
            Possible reasons are:
             - Communication with Travis CI has failed.
             - Insufficient permissions.
             - Invalid contents returned.
    ''')[1:]

    response._content = b'{"error": "foo"}'
    with pytest.raises(TravisError) as exception_info:
        get_response_contents(response)
    assert str(exception_info.value) == '[111] foo'

    response.status_code = 200
    assert get_response_contents(response) == {'error': 'foo'}
