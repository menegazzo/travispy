from .errors import TravisError
import textwrap


def get_response_contents(response, exception_=TravisError):
    '''
    :type response: :class:`requests.models.Response`
    :param response:
        Response returned from Travis API.

    :type exception_: :class:`.TravisError`
    :param exception:
        Exception that should be raised when return code is different than 200.

    :rtype: dict
    :returns:
        Content related the request related to the given ``response``.

    :raises TravisError: when return code is different than 200 or an unexpected error happens.
    '''
    status_code = response.status_code
    try:
        contents = response.json()
    except:
        contents = {
            'status_code': status_code,
            'error': textwrap.dedent('''
                Unexpected error
                    Possible reasons are:
                     - Communication with Travis CI has failed.
                     - Insufficient permissions.
                     - Invalid contents returned.
                ''')[1:],
        }
        raise TravisError(contents)

    if status_code == 200:
        return contents
    else:
        contents['status_code'] = status_code
        raise exception_(contents)
