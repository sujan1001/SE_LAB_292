"""Line/code-coverage tests for the Lab 6 bike-share application."""

import pytest

from bike_share_rental import can_unlock, dock_status, ride_cost


def test_ride_cost_validation():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("tandem", 30, False, False)
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)


def test_ride_cost_regular_and_subscriber_paths():
    assert ride_cost("standard", 45, False, False) == 40
    assert ride_cost("electric", 60, True, False) == 35
    assert ride_cost("standard", 15, True, False) == 0


def test_ride_cost_peak_and_long_ride_paths():
    assert ride_cost("electric", 30, False, True) == 50
    assert ride_cost("standard", 181, False, False) == 240


def test_dock_status_validation_and_states():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(11, 10)

    assert dock_status(0, 10) == "empty"
    assert dock_status(10, 10) == "full"
    assert dock_status(2, 10) == "few bikes"
    assert dock_status(8, 10) == "few slots"
    assert dock_status(5, 10) == "available"


def test_can_unlock_representative_paths():
    assert can_unlock(1000, True, 30) is False
    assert can_unlock(1000, False, 15) is False
    assert can_unlock(100, False, 17) is True
    assert can_unlock(50, False, 18) is True
