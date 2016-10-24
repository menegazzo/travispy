from travispy.errors import TravisError


class Tests:

    def test_status_code(self):
        error = TravisError({'status_code': 404, 'error': 'Not Found'})
        assert error.status_code == 404
