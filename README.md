# Cohort Validator

A Python package providing an interface to the OHDSI CIRCE (Cohort Inclusion Rule and Cohort Expression) library for validating cohort definitions.

## Features

- **Cohort Validation**: Validate cohort expressions using the OHDSI CIRCE library
- **Python Interface**: Easy-to-use Python API for cohort validation
- **Command Line Tool**: CLI for validating cohort JSON files
- **Comprehensive Testing**: Extensive test suite with real-world examples
- **Package Distribution**: Installable Python package with proper dependencies

## Installation

### Prerequisites

- Python 3.8 or higher
- Java 8 or higher (for CIRCE library)
- Maven (for building CIRCE JAR files)

### Install from GitHub (Recommended)

```bash
# Install directly from GitHub
pip install git+https://github.com/epam/ohdsi-cohort-validator.git

# Install with development dependencies
pip install git+https://github.com/epam/ohdsi-cohort-validator.git[dev]

# Install specific version (if tagged)
pip install git+https://github.com/epam/ohdsi-cohort-validator.git@v1.0.0
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/epam/ohdsi-cohort-validator.git
cd ohdsi-cohort-validator

# Set up the environment and build dependencies
make setup

# Install the package in development mode
make install
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build CIRCE JAR files
make build-jar

# Install package
pip install -e .
```

## Usage

### Python API

```python
from cohort_validator import CohortValidator

# Initialize validator
validator = CohortValidator()

# Validate a cohort expression
cohort_data = {
    "conceptSets": [
        {
            "id": 1,
            "name": "Test Concept Set",
            "expression": {
                "items": []
            }
        }
    ],
    "primaryCriteria": {
        "criteriaList": []
    }
}

warnings, errors = validator.validate_cohort(cohort_data)

print(f"Warnings: {len(warnings)}")
print(f"Errors: {len(errors)}")

for error in errors:
    print(f"Error: {error['message']}")
```

### Command Line Interface

```bash
# Validate a cohort JSON file
cohort-validate cohort.json

# Output to file with text format
cohort-validate cohort.json --output results.txt --format text

# Specify custom JAR paths
cohort-validate cohort.json --jar-path /path/to/circe.jar --deps-path /path/to/deps
```

## Development

### Running Tests

```bash
# Run all tests
make test

# Run specific test suites
make test-basic
make test-final
make test-comprehensive

# Run tests with coverage
make test-coverage
```

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check
```

### Building Package

```bash
# Build distribution packages
make build

# Clean build artifacts
make clean-build
```

## Project Structure

```
cohort-validator/
├── cohort_validator/         # Main package
│   ├── __init__.py           # Package initialization
│   ├── cohort_validator.py   # Core validation logic
│   ├── cli.py               # Command-line interface
│   └── tests/               # Test suite
│       ├── test_validator.py
│       ├── test_final.py
│       └── test_comprehensive.py
├── circe-be/                # CIRCE Java library (cloned)
├── setup.py                 # Package setup
├── pyproject.toml          # Modern Python packaging
├── requirements.txt        # Dependencies
├── Makefile               # Build automation
└── README.md              # This file
```

## API Reference

### CohortValidator

The main class for validating cohort expressions.

#### Constructor

```python
CohortValidator(jar_path=None, deps_path=None)
```

- `jar_path`: Path to CIRCE JAR file (auto-detected if not provided)
- `deps_path`: Path to CIRCE dependencies directory (auto-detected if not provided)

#### Methods

##### `validate_cohort(cohort_json: dict) -> Tuple[List[Dict], List[Dict]]`

Validate a cohort expression and return warnings and errors.

**Parameters:**
- `cohort_json`: Dictionary containing the cohort expression

**Returns:**
- Tuple of (warnings, errors) where each is a list of dictionaries containing:
  - `message`: Description of the issue
  - `severity`: Severity level (WARNING, ERROR, etc.)
  - `type`: Type of validation issue

## Validation Types

The library can detect various types of validation issues:

- **Unused Concept Sets**: Concept sets that are defined but not used
- **Empty Values**: Missing or empty required fields
- **Duplicate Criteria**: Duplicate criteria in the same group
- **Time Window Issues**: Invalid time window configurations
- **Missing Criteria**: Required criteria that are missing
- **Contradictions**: Conflicting criteria or settings
- **Domain Type Issues**: Incorrect domain types for criteria
- **Range Validation**: Invalid numeric ranges
- **Exit Criteria**: Missing or invalid exit criteria
- **Events Progression**: Issues with event progression logic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `make test`
6. Format code: `make format`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OHDSI CIRCE](https://github.com/OHDSI/circe-be) - The underlying Java library for cohort validation
- [JPype](https://github.com/jpype-project/jpype) - Python-Java bridge library