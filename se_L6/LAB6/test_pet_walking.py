import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars


# ---------------------------------------------------------------------------
# Tests for process_walking_routes
# ---------------------------------------------------------------------------

def test_routes_invalid_type_raises_value_error():
    """Verify ValueError is raised when routes is not a list."""
    with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
        process_walking_routes("not_a_list", 5.0)

    with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
        process_walking_routes(None, 5.0)


def test_negative_base_transport_fee_raises_value_error():
    """Verify ValueError is raised when base_transport_fee is negative."""
    with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
        process_walking_routes([], -0.01)


def test_empty_routes_returns_zero_earnings():
    """Verify empty routes list returns ZERO_EARNINGS status with 0.0 revenue."""
    result = process_walking_routes([], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_unconfirmed_route_is_skipped():
    """Verify route is skipped if route_confirmed is False or omitted."""
    routes = [
        {
            "route_confirmed": False,
            "session_type": "standard_30",
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        },
        {
            # route_confirmed omitted -> defaults to False
            "session_type": "standard_30",
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_unknown_session_type_increments_incident_and_skips():
    """Verify unrecognized session type increments incident count and skips route."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "vip_90",  # Unrecognized session type
            "walks": [{"num_pets": 1}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_single_standard_30_walk():
    """Starter test: single standard 30 walk with 1 pet."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    # base_fee: 22.0 + (1 * 5.0) = 27.0
    assert result["total_revenue"] == 27.0
    assert result["status"] == "COMPLETED"


def test_default_session_type_and_empty_walks():
    """Verify default session_type is standard_30 and route with no walks has zero route earnings."""
    routes = [
        {
            "route_confirmed": True,
            # session_type omitted -> standard_30 (base 22.0)
            "is_weekend": True,
            # walks omitted -> []
        }
    ]
    result = process_walking_routes(routes, 10.0)
    # route_earnings: 0.0 from walks + 10.0 weekend transport fee = 10.0
    assert result["total_revenue"] == 10.0
    assert result["status"] == "COMPLETED"


def test_express_15_session_with_medication():
    """Verify express_15 session base fee and medication surcharge."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "express_15",
            "is_weekend": False,
            "walks": [
                {"num_pets": 2, "aggression_alert": False, "needs_meds": True}
            ]
        }
    ]
    # base_fee: 14.0 + (2 * 5.0) = 24.0; meds: +6.0 => 30.0
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 30.0
    assert result["status"] == "COMPLETED"


def test_standard_60_session_with_more_than_3_pets():
    """Verify standard_60 base fee and pet discount calculation when num_pets > 3."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_60",
            "is_weekend": False,
            "walks": [
                {"num_pets": 4, "aggression_alert": False, "needs_meds": False}
            ]
        }
    ]
    # base_fee: 35.0; (35.0 + 4 * 8.0) * 0.90 = (35.0 + 32.0) * 0.90 = 67.0 * 0.90 = 60.3
    result = process_walking_routes(routes, 0.0)
    assert result["total_revenue"] == 60.3
    assert result["status"] == "COMPLETED"


def test_invalid_num_pets_increments_incident():
    """Verify walk with num_pets <= 0 increments incident count and is skipped."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "walks": [
                {"num_pets": 0},   # invalid, incident
                {"num_pets": -1},  # invalid, incident
                {"num_pets": 1, "aggression_alert": False, "needs_meds": False}
            ]
        }
    ]
    # only the 3rd walk is billed: 22.0 + 5.0 = 27.0
    result = process_walking_routes(routes, 0.0)
    assert result["total_revenue"] == 27.0
    assert result["status"] == "COMPLETED"


def test_aggression_alert_standard_60_aborts_route():
    """Verify aggression alert in standard_60 resets route earnings to 0 and breaks."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_60",
            "is_weekend": False,
            "walks": [
                {"num_pets": 2, "aggression_alert": False, "needs_meds": False},  # would be 45.0
                {"num_pets": 1, "aggression_alert": True, "needs_meds": True},   # causes break & reset
                {"num_pets": 1, "aggression_alert": False, "needs_meds": False}  # unreachable walk
            ]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"


def test_aggression_alert_non_standard_60_adds_zero_and_continues():
    """Verify aggression alert in non-standard_60 adds 0 earnings and checks meds."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [
                {"num_pets": 2, "aggression_alert": True, "needs_meds": True},
                {"num_pets": 1, "aggression_alert": False, "needs_meds": False}
            ]
        }
    ]
    # Walk 1: aggression alert -> route_earnings += 0.0, needs_meds is True -> +6.0
    # Walk 2: 22.0 + 5.0 = 27.0
    # Total = 33.0
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 33.0
    assert result["status"] == "COMPLETED"


def test_weekend_fee_added_to_route():
    """Verify weekend route adds base_transport_fee."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": True,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    # 22 + 5 = 27 + 8.5 transport fee = 35.5
    result = process_walking_routes(routes, 8.5)
    assert result["total_revenue"] == 35.5
    assert result["status"] == "COMPLETED"


def test_incident_audit_when_incident_count_exceeds_four():
    """Verify status is INCIDENT_AUDIT when incident_count > 4."""
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "walks": [
                {"num_pets": 0},  # incident 1
                {"num_pets": 0},  # incident 2
                {"num_pets": 0},  # incident 3
                {"num_pets": 0},  # incident 4
                {"num_pets": 0},  # incident 5
                {"num_pets": 1, "aggression_alert": False, "needs_meds": False}
            ]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["status"] == "INCIDENT_AUDIT"
    assert result["total_revenue"] == 27.0


# ---------------------------------------------------------------------------
# Tests for inspect_gps_collars
# ---------------------------------------------------------------------------

def test_inspect_gps_collars_empty_or_none():
    """Verify NO_DATA is returned when collar matrix is empty or falsy."""
    assert inspect_gps_collars([]) == "NO_DATA"
    assert inspect_gps_collars(None) == "NO_DATA"


def test_inspect_gps_collars_all_online():
    """Verify ONLINE is returned when all signals remain at or above 20."""
    collar_matrix = [
        [25, 40, 80],
        [20, 21, 30]
    ]
    assert inspect_gps_collars(collar_matrix) == "ONLINE"


def test_inspect_gps_collars_empty_sublog():
    """Verify ONLINE is returned when collar matrix contains empty sublogs."""
    assert inspect_gps_collars([[]]) == "ONLINE"


def test_inspect_gps_collars_streak_reset():
    """Verify signal lost streak resets if a strong signal occurs between weak signals."""
    collar_matrix = [
        [15, 25, 10, 30, 19]  # weak, strong, weak, strong, weak -> streak never reaches 2
    ]
    assert inspect_gps_collars(collar_matrix) == "ONLINE"


def test_inspect_gps_collars_lost_signal_alert():
    """Verify LOST_SIGNAL_ALERT is returned when signal is below 20 for 2+ consecutive logs."""
    collar_matrix = [
        [50, 60, 70],
        [30, 15, 10, 40]  # two consecutive signals < 20
    ]
    assert inspect_gps_collars(collar_matrix) == "LOST_SIGNAL_ALERT"


def test_inspect_gps_collars_lost_signal_alert_immediate():
    """Verify LOST_SIGNAL_ALERT triggered at the very start of a collar log."""
    collar_matrix = [
        [10, 5]
    ]
    assert inspect_gps_collars(collar_matrix) == "LOST_SIGNAL_ALERT"
