"""Pet Walking Service - Hardened against input validation bugs (Lab 7).

Every function validates its input defensively and returns None for invalid
or malformed input instead of raising exceptions, preventing crashes.
"""
import math
import re

_SCHEDULE_RE = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*-\s*([A-Za-z]+)\s*$")
_METRICS_RE = re.compile(r"^\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*/\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*$")

WEEKEND_MAP = {"YES": 15.0, "NO": 0.0}
SURCHARGES = {
    "CAL": 0.0,
    "PLY": 5.0,
    "PLA": 5.0,  # Fix for 'PLAYFUL' whose first 3 letters are 'PLA'
    "REA": 12.0,
    "AGG": 20.0
}


def parse_walk_schedule(schedule_spec):
    """Parses '<pets>-<mins>-<weekend>' schedule string.
    Returns formatted summary string on valid input, or None on invalid input.
    """
    if not isinstance(schedule_spec, str):
        return None
    match = _SCHEDULE_RE.match(schedule_spec)
    if not match:
        return None
    try:
        pets = int(match.group(1))
        mins = int(match.group(2))
    except (ValueError, OverflowError):
        return None
    
    if pets < 0 or mins < 0:
        return None

    weekend_token = match.group(3).strip().upper()
    if weekend_token not in WEEKEND_MAP:
        return None
    weekend_fee = WEEKEND_MAP[weekend_token]

    base_fee = 20.0 if mins <= 30 else 35.0
    total = base_fee + (pets * 5.0) + weekend_fee
    return f"Walk: {pets} pets, {mins} mins - Total ${total:.2f}"


def compute_pace_per_pet(walk_metrics_str):
    """Computes pace per pet given '<mins>/<pets>'.
    Returns round(mins / pets, 2) on valid input, or None on invalid input.
    """
    if not isinstance(walk_metrics_str, str):
        return None
    match = _METRICS_RE.match(walk_metrics_str)
    if not match:
        return None
    try:
        mins = float(match.group(1))
        pets = float(match.group(2))
    except (ValueError, OverflowError):
        return None
    
    if not (math.isfinite(mins) and math.isfinite(pets)):
        return None
    if mins < 0 or pets <= 0:
        return None
    
    pace = mins / pets
    if not math.isfinite(pace):
        return None
    return round(pace, 2)


def lookup_temperament_surcharge(temperament_code):
    """Looks up temperament surcharge for CAL, PLY/PLA, REA, AGG prefixes.
    Returns surcharge float on valid input, or None on invalid input.
    """
    if not isinstance(temperament_code, str):
        return None
    cleaned = temperament_code.strip().upper()
    if len(cleaned) < 3:
        return None
    prefix = cleaned[:3]
    return SURCHARGES.get(prefix, None)


def main():
    print("==== Running parse_walk_schedule ====")
    s_input = input("Enter schedule (e.g. 2-30-YES): ")
    result = parse_walk_schedule(s_input)
    print(result if result is not None else "Invalid schedule format (expected <pets>-<mins>-YES/NO)")

    print("\n==== Running compute_pace_per_pet ====")
    p_input = input("Enter minutes/pets (e.g. 45/3): ")
    result = compute_pace_per_pet(p_input)
    print("Pace (min/pet):", result if result is not None else "Invalid metrics format (expected <mins>/<pets>, pets > 0)")

    print("\n==== Running lookup_temperament_surcharge ====")
    t_input = input("Enter temperament code (e.g. CALM, PLAYFUL, AGGRESSIVE): ")
    result = lookup_temperament_surcharge(t_input)
    print("Surcharge: $", result if result is not None else "Invalid temperament code")


if __name__ == "__main__":
    main()
