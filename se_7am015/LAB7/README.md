# Lab 7 — Fuzzing for Input Validation Bugs

**Course:** Software Engineering Lab (SE Lab)  
**Student:** Aditya Shet  
**USN:** PES2UG24AM015  
**Assigned Repo:** `SETAPESU26/L6_L7_13_pet_walking_service` (Lab 7: Pet Walking Service)  
**Tools:** Hypothesis 6.170 + pytest 9.1

---

## Overview

A set of property-based fuzz tests targeting pet walk schedule tokens, pace-per-pet calculations, and pet temperament handling surcharges to uncover and resolve input validation flaws using the Hypothesis fuzzing framework.

## Project Structure

```text
se_7am015/
├── processor.py                   # Hardened application (defensive input validation)
├── test_processor.py              # Completed Hypothesis fuzz test suite (11 tests, 500 examples each)
├── README.md                      # Comprehensive Lab 7 documentation and results
├── generate_artifacts.py          # Script to run all steps, render screenshots, and build PDF
├── Lab7_Submission.pdf            # 2-Page formal submission report with embedded screenshots
├── original/
│   └── processor.py               # Original buggy starter code
├── screenshots/
│   ├── step2_original_run.png     # Screenshot of Step 2 (running original code + crash demonstration)
│   ├── step4_tests_failing.png    # Screenshot of Step 4 (Hypothesis fuzz tests failing vs original code)
│   ├── step5_fixed_run.png        # Screenshot of Step 5 (running fixed application defensively)
│   └── step6_tests_passing.png    # Screenshot of Step 6 (all 11 Hypothesis tests passing vs fixed code)
└── LAB7/                          # Archive directory containing copies of all deliverables
    ├── processor.py
    ├── test_processor.py
    ├── README.md
    ├── Lab7_Submission.pdf
    └── screenshots/
```

---

## Lab Steps & Verification

### Step 1: Installing Dependencies
```bash
pip install hypothesis pytest reportlab pillow
```

### Step 2: Running the Original Application
Running the original application with normal inputs produces output, but empty or malformed inputs cause unhandled exceptions:
- `""` or invalid format triggers `ValueError: not enough values to unpack (expected 3, got 1)`.
- `None` triggers `AttributeError: 'NoneType' object has no attribute 'strip'`.

Screenshot captured in `screenshots/step2_original_run.png`.

### Step 3: Completing `test_processor.py` with Hypothesis
The test suite consists of 11 tests configured with `@settings(max_examples=500, deadline=None)`:
1. **No-Crash Fuzzers (try/except):**
   - `test_parse_walk_schedule_no_crash(s)`
   - `test_compute_pace_per_pet_safe(s)`
   - `test_lookup_temperament_surcharge_safe(s)`
2. **Property-Based Validation Tests:**
   - `test_parse_walk_schedule_valid`: verifies exact formula `base_fee + pets * 5.0 + weekend_fee`.
   - `test_parse_walk_schedule_rejects_bad_weekend`: rejects invalid weekend strings.
   - `test_parse_walk_schedule_rejects_negative_pets`: rejects negative pet counts.
   - `test_compute_pace_per_pet_valid`: verifies `round(mins / pets, 2)`.
   - `test_compute_pace_per_pet_zero_division`: verifies rejection of `pets == 0`.
   - `test_compute_pace_per_pet_rejects_non_finite`: rejects `NaN`, `Inf`, `-Inf`.
   - `test_lookup_temperament_surcharge_valid`: verifies valid prefixes (`CAL`, `PLY`, `PLA`, `REA`, `AGG`).
   - `test_lookup_temperament_surcharge_unknown`: verifies rejection of unknown codes.

### Step 4: Running Fuzz Tests Against Original Code
```bash
python -m pytest test_processor.py
```
**Result:** 9 failed, 2 passed.  
Hypothesis discovered minimal failing examples for each flaw.  
Screenshot captured in `screenshots/step4_tests_failing.png`.

### Step 5: Hardening `processor.py`
**Design Principle:** All functions validate input defensively using regex, strict type checking, and mathematical constraints. If input is malformed or invalid, the functions return `None` rather than raising unhandled exceptions. The `main()` CLI driver handles `None` gracefully and prints helpful user messages.

Screenshot captured in `screenshots/step5_fixed_run.png`.

### Step 6: Re-Running Fuzz Tests Against Fixed Code
```bash
python -m pytest test_processor.py -v
```
**Result:** All 11 passed (100% success rate across 5,500 generated test cases).  
Screenshot captured in `screenshots/step6_tests_passing.png`.

---

## Bugs Uncovered and Applied Fixes

| Function | Minimal Failing Input | Original Behaviour | Hardened Defensive Fix |
|---|---|---|---|
| `parse_walk_schedule` | `None` | `AttributeError: 'NoneType' object has no attribute 'strip'` | Type check `isinstance(s, str)` → `None` |
| `parse_walk_schedule` | `""`, `"2-30"` | `ValueError: not enough values to unpack` | Regex pattern matching (`^\s*(\d+)\s*-\s*(\d+)\s*-\s*([A-Za-z]+)\s*$`) → `None` |
| `parse_walk_schedule` | `"a-b-YES"` | `ValueError: invalid literal for int()` | Safe integer parsing with exception handling → `None` |
| `parse_walk_schedule` | `"-1-30-YES"` | Incorrect token splitting / negative pet count | Strict non-negative range check `pets >= 0 and mins >= 0` → `None` |
| `parse_walk_schedule` | `"2-30-MAYBE"` | `KeyError: 'MAYBE'` | Explicit validation against `{"YES": 15.0, "NO": 0.0}` → `None` |
| `compute_pace_per_pet` | `None`, `""` | `AttributeError` / `ValueError` | Type check and regex pattern `mins/pets` validation → `None` |
| `compute_pace_per_pet` | `"45/0"` | `ZeroDivisionError: float division by zero` | Explicit check `pets <= 0` → `None` |
| `compute_pace_per_pet` | `"nan/2"`, `"1e400/2"` | Returns `nan` / `inf` | `math.isfinite()` validation on inputs and result → `None` |
| `lookup_temperament_surcharge` | `None`, `""`, `"CA"` | `AttributeError` / `KeyError` | Type check & minimum length `>= 3` check → `None` |
| `lookup_temperament_surcharge` | `"PLAYFUL"` | `KeyError: 'PLA'` (dict only contained `'PLY'`) | Supported both `'PLA'` and `'PLY'` mapped to `5.0` |
| `lookup_temperament_surcharge` | `"UNKNOWN"` | `KeyError: 'UNK'` | Dictionary lookup with `SURCHARGES.get(prefix, None)` → `None` |

---

## Deliverables Summary

1. **Submission PDF:** `Lab7_Submission.pdf` (and `LAB7/Lab7_Submission.pdf`)
2. **Fixed Application:** `processor.py` (and `LAB7/processor.py`)
3. **Completed Test Suite:** `test_processor.py` (and `LAB7/test_processor.py`)
4. **All Screenshots:** Located in `screenshots/` and `LAB7/screenshots/`:
   - `step2_original_run.png`
   - `step4_tests_failing.png`
   - `step5_fixed_run.png`
   - `step6_tests_passing.png`
