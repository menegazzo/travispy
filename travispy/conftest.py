import json
import os
import pytest


@pytest.fixture(scope='session')
def test_settings():
    '''
    Test settings must be given in JSON format.

    The environment variable ``TRAVISPY_TEST_SETTINGS`` may receive JSON content directly or just
    point to a file following the same format.

    The file ``test_settings.example.json`` provides a template for the expected information.
    '''
    test_settings = os.environ.get('TRAVISPY_TEST_SETTINGS', '')
    if os.path.isfile(test_settings):
        with open(test_settings) as f:
            test_settings = f.read()

    if not test_settings.strip():
        pytest.skip('TRAVISPY_TEST_SETTINGS environment variable is not set')

    try:
        test_settings = json.loads(test_settings)
    except ValueError:
        pytest.skip('TRAVISPY_TEST_SETTINGS is bad formated')

    return test_settings


@pytest.fixture
def repo_slug(test_settings):
    repo_slug = test_settings.get('repo_slug')
    if not repo_slug:
        pytest.skip('TRAVISPY_TEST_SETTINGS has no "repo_slug" value')
    return repo_slug
