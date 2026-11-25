# L6_L7_13 — Pet Walking Service

Lab 6: Code and Branch Coverage

## About

A small Python module that bills pet walking appointments based on duration, pet count, behavioral flags, and medication needs, and verifies collar GPS tracker signals.

## Files

| File | Description |
|------|-------------|
| `pet_walking_service.py` | The module under test |
| `test_pet_walking.py` | Test suite achieving 100% Line and 100% Branch Coverage |
| `output_screenshot.png` | Terminal screenshot showing test execution and 100% coverage |
| `coverage_report.png` | Detailed coverage table screenshot |

## Running Tests and Coverage

To run the full test suite with line and branch coverage report:

```bash
pytest -v --cov=pet_walking_service --cov-branch --cov-report=term-missing
```

## Results Summary

- **Total Test Cases**: 20 (All Passed)
- **Line/Statement Coverage**: 100% (57/57 statements)
- **Branch Coverage**: 100% (40/40 branches)
