"""Lab 7 - Hypothesis fuzz tests for processor.py (Pet Walking Service).

Contract for the hardened module: invalid input returns None (never raises);
valid input returns the correct computed value or formatted string.
"""
import math
from hypothesis import given, settings, strategies as st
from processor import parse_walk_schedule, compute_pace_per_pet, lookup_temperament_surcharge

FUZZ = settings(max_examples=500, deadline=None)

# ---------------- 1. No-crash fuzzing (random / malformed inputs) ----------------
@FUZZ
@given(st.text() | st.none())
def test_parse_walk_schedule_no_crash(s):
    # To-Do:Using try and except complete this function.
    try:
        parse_walk_schedule(s)
    except Exception as e:
        assert False, f"parse_walk_schedule crashed on {s!r}: {e!r}"


@FUZZ
@given(st.text() | st.none())
def test_compute_pace_per_pet_safe(s):
    # To-Do:Using try and except complete this function.
    try:
        compute_pace_per_pet(s)
    except Exception as e:
        assert False, f"compute_pace_per_pet crashed on {s!r}: {e!r}"


@FUZZ
@given(st.text() | st.none())
def test_lookup_temperament_surcharge_safe(s):
    # To-Do:Using try and except complete this function.
    try:
        lookup_temperament_surcharge(s)
    except Exception as e:
        assert False, f"lookup_temperament_surcharge crashed on {s!r}: {e!r}"


# ---------------- 2. Property tests (correctness & input validation) ----------------
@FUZZ
@given(
    st.integers(min_value=0, max_value=50),
    st.integers(min_value=0, max_value=240),
    st.sampled_from(["YES", "NO", "yes", "no", " Yes ", " No "])
)
def test_parse_walk_schedule_valid(pets, mins, weekend):
    res = parse_walk_schedule(f"{pets}-{mins}-{weekend}")
    expected_base = 20.0 if mins <= 30 else 35.0
    expected_weekend = 15.0 if weekend.strip().upper() == "YES" else 0.0
    expected_total = expected_base + (pets * 5.0) + expected_weekend
    assert res == f"Walk: {pets} pets, {mins} mins - Total ${expected_total:.2f}"


@FUZZ
@given(st.integers(0, 10), st.integers(0, 60), st.text().filter(lambda x: x.strip().upper() not in ["YES", "NO"]))
def test_parse_walk_schedule_rejects_bad_weekend(pets, mins, bad_weekend):
    assert parse_walk_schedule(f"{pets}-{mins}-{bad_weekend}") is None


@FUZZ
@given(st.integers(-100, -1), st.integers(0, 60))
def test_parse_walk_schedule_rejects_negative_pets(pets, mins):
    assert parse_walk_schedule(f"{pets}-{mins}-NO") is None


@FUZZ
@given(
    st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.1, max_value=50.0, allow_nan=False, allow_infinity=False)
)
def test_compute_pace_per_pet_valid(mins, pets):
    res = compute_pace_per_pet(f"{mins}/{pets}")
    expected = round(mins / pets, 2)
    assert res == expected


@FUZZ
@given(st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False))
def test_compute_pace_per_pet_zero_division(mins):
    assert compute_pace_per_pet(f"{mins}/0") is None
    assert compute_pace_per_pet(f"{mins}/0.0") is None


@FUZZ
@given(st.sampled_from(["nan", "inf", "-inf", "1e400"]))
def test_compute_pace_per_pet_rejects_non_finite(bad):
    assert compute_pace_per_pet(f"{bad}/2") is None
    assert compute_pace_per_pet(f"30/{bad}") is None


@FUZZ
@given(st.sampled_from([
    "CALM", "CAL", "calm", "cal",
    "PLAYFUL", "PLY", "playful", "ply",
    "REACTIVE", "REA", "reactive", "rea",
    "AGGRESSIVE", "AGG", "aggressive", "agg"
]))
def test_lookup_temperament_surcharge_valid(code):
    expected_map = {"CAL": 0.0, "PLY": 5.0, "PLA": 5.0, "REA": 12.0, "AGG": 20.0}
    prefix = code.strip().upper()[:3]
    assert lookup_temperament_surcharge(code) == expected_map[prefix]


@FUZZ
@given(st.text(min_size=1, max_size=20).filter(lambda s: s.strip().upper()[:3] not in ["CAL", "PLY", "PLA", "REA", "AGG"]))
def test_lookup_temperament_surcharge_unknown(code):
    assert lookup_temperament_surcharge(code) is None
