from travispy.entities._stateful import Stateful
import pytest


#===================================================================================================
# Test
#===================================================================================================
class Test:

    @pytest.mark.parametrize(
        'state, color, expected_true_properties', [
        (Stateful.CREATED, Stateful.YELLOW, (Stateful.CREATED, Stateful.YELLOW, 'pending')),
        (Stateful.QUEUED, Stateful.YELLOW, (Stateful.CREATED, Stateful.QUEUED, Stateful.YELLOW, 'pending')),
        (Stateful.STARTED, Stateful.YELLOW, (Stateful.CREATED, Stateful.QUEUED, Stateful.STARTED, Stateful.YELLOW, 'pending', 'running')),
        (Stateful.PASSED, Stateful.GREEN, (Stateful.CREATED, Stateful.QUEUED, Stateful.STARTED, Stateful.PASSED, Stateful.GREEN, 'finished', 'successful')),
        (Stateful.FAILED, Stateful.RED, (Stateful.CREATED, Stateful.QUEUED, Stateful.STARTED, Stateful.FAILED, Stateful.RED, 'finished', 'unsuccessful')),
        (Stateful.ERRORED, Stateful.RED, (Stateful.CREATED, Stateful.QUEUED, Stateful.STARTED, Stateful.ERRORED, Stateful.RED, 'finished', 'unsuccessful')),
        (Stateful.CANCELED, Stateful.RED, (Stateful.CREATED, Stateful.QUEUED, Stateful.STARTED, Stateful.CANCELED, Stateful.RED, 'finished', 'unsuccessful')),
        (Stateful.READY, Stateful.GREEN, (Stateful.CREATED, Stateful.QUEUED, Stateful.STARTED, Stateful.READY, Stateful.GREEN, 'finished')),
    ])
    def test_stateful(self, state, color, expected_true_properties):
        stateful = Stateful(None)

        assert hasattr(stateful, 'state') == False
        with pytest.raises(AttributeError):
            stateful.created

        stateful.state = None
        with pytest.raises(ValueError):
            stateful.created

        stateful.state = state
        assert stateful.color == color
        
        for prop in [
            Stateful.CREATED,
            Stateful.QUEUED,
            Stateful.STARTED,
            Stateful.PASSED,
            Stateful.FAILED,
            Stateful.ERRORED,
            Stateful.CANCELED,
            Stateful.READY,
            Stateful.GREEN,
            Stateful.YELLOW,
            Stateful.RED,
            'pending',
            'running',
            'finished',
            'successful',
            'unsuccessful',
            ]:
            assert getattr(stateful, prop) == (prop in expected_true_properties)
