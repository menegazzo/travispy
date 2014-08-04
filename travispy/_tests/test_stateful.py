from travispy.entities._stateful import Stateful
import pytest


#===================================================================================================
# Test
#===================================================================================================
class Test:

    @pytest.mark.parametrize(
        'state, created, queued, started, passed, failed, errored, canceled, ready, pending, running, finished, successful, unsuccessful, color, green, yellow, red', [
        (Stateful.CREATED, True, False, False, False, False, False, False, False, True, False, False, False, False, Stateful.YELLOW, False, True, False),
        (Stateful.QUEUED, True, True, False, False, False, False, False, False, True, False, False, False, False, Stateful.YELLOW, False, True, False),
        (Stateful.STARTED, True, True, True, False, False, False, False, False, True, True, False, False, False, Stateful.YELLOW, False, True, False),
        (Stateful.PASSED, True, True, True, True, False, False, False, False, False, False, True, True, False, Stateful.GREEN, True, False, False),
        (Stateful.FAILED, True, True, True, False, True, False, False, False, False, False, True, False, True, Stateful.RED, False, False, True),
        (Stateful.ERRORED, True, True, True, False, False, True, False, False, False, False, True, False, True, Stateful.RED, False, False, True),
        (Stateful.CANCELED, True, True, True, False, False, False, True, False, False, False, True, False, True, Stateful.RED, False, False, True),
        (Stateful.READY, True, True, True, False, False, False, False, True, False, False, True, False, False, Stateful.GREEN, True, False, False),
    ])
    def testStateful(self, state, created, queued, started, passed, failed, errored, canceled, ready, pending, running, finished, successful, unsuccessful, color, green, yellow, red):
        stateful = Stateful(None)

        assert hasattr(stateful, 'state') == False
        with pytest.raises(AttributeError):
            stateful.created

        stateful.state = None
        with pytest.raises(ValueError):
            stateful.created

        stateful.state = state
        assert stateful.created == created
        assert stateful.queued == queued
        assert stateful.started == started
        assert stateful.passed == passed
        assert stateful.failed == failed
        assert stateful.errored == errored
        assert stateful.canceled == canceled
        assert stateful.ready == ready
        assert stateful.pending == pending
        assert stateful.running == running
        assert stateful.finished == finished
        assert stateful.successful == successful
        assert stateful.unsuccessful == unsuccessful
        assert stateful.color == color
        assert stateful.green == green
        assert stateful.yellow == yellow
        assert stateful.red == red
