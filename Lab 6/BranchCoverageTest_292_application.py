"""Branch-coverage tests for the Lab 6 bike-share application."""

import pytest

from bike_share_rental import can_unlock, dock_status, ride_cost


@pytest.mark.parametrize(
    ("bike_type", "minutes", "is_subscriber", "is_peak", "expected"),
    [
        ("standard", 45, False, False, 40),
        ("electric", 60, True, False, 35),
        ("standard", 15, True, False, 0),
        ("electric", 30, False, True, 50),
        ("cargo", 30, False, True, 50),
        ("standard", 181, False, False, 240),
    ],
)
def test_ride_cost_branches(bike_type, minutes, is_subscriber, is_peak, expected):
    assert ride_cost(bike_type, minutes, is_subscriber, is_peak) == expected


@pytest.mark.parametrize(
    ("bike_type", "minutes", "message"),
    [
        ("tandem", 30, "unknown bike type"),
        ("standard", 0, "invalid duration"),
    ],
)
def test_ride_cost_error_branches(bike_type, minutes, message):
    with pytest.raises(ValueError, match=message):
        ride_cost(bike_type, minutes, False, False)


@pytest.mark.parametrize(
    ("bikes_docked", "capacity", "expected"),
    [
        (0, 10, "empty"),
        (10, 10, "full"),
        (1, 10, "few bikes"),
        (2, 10, "few bikes"),
        (8, 10, "few slots"),
        (9, 10, "few slots"),
        (5, 10, "available"),
    ],
)
def test_dock_status_result_branches(bikes_docked, capacity, expected):
    assert dock_status(bikes_docked, capacity) == expected


@pytest.mark.parametrize(
    ("bikes_docked", "capacity", "message"),
    [
        (0, 0, "invalid capacity"),
        (-1, 10, "invalid bike count"),
        (11, 10, "invalid bike count"),
    ],
)
def test_dock_status_error_branches(bikes_docked, capacity, message):
    with pytest.raises(ValueError, match=message):
        dock_status(bikes_docked, capacity)


@pytest.mark.parametrize(
    ("balance", "active", "age", "expected"),
    [
        (1000, True, 30, False),
        (1000, False, 15, False),
        (99, False, 17, False),
        (100, False, 17, True),
        (49, False, 18, False),
        (50, False, 18, True),
    ],
)
def test_can_unlock_branches(balance, active, age, expected):
    assert can_unlock(balance, active, age) is expected
