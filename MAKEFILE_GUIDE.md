# Makefile Guide for Cohort Validator

## 🚀 **Quick Start Commands**

### **Essential Commands**
```bash
# Set up everything (recommended for first time)
make setup

# Run quick basic tests
make test-quick

# Run comprehensive test (recommended)
make test-final

# Run all tests
make test
```

### **Build Commands**
```bash
# Build Java JAR files and dependencies
make build-jar

# Clean Java build artifacts
make clean-java

# Clean everything
make clean
```

### **Test Commands**
```bash
# Basic functionality tests
make test-basic

# Final comprehensive test (RECOMMENDED)
make test-final

# Simple comprehensive test
make test-comprehensive

# Validation scenario tests
make test-scenarios

# Full comprehensive test
make test-full

# Individual test files
make test-validator
make test-simple
make test-validation
```

### **Utility Commands**
```bash
# Show help
make help

# Check dependencies
make check-deps

# Show project status
make status

# List available tests
make list-tests

# Validate a specific cohort file
make validate-cohort FILE=path/to/cohort.json

# Run example usage
make example
```

## 📋 **Available Make Targets**

| Command | Description |
|---------|-------------|
| `make setup` | Set up complete environment (venv, dependencies, JAR files) |
| `make test-quick` | Run quick basic tests only |
| `make test-final` | Run final comprehensive test (RECOMMENDED) |
| `make test` | Run all test suites |
| `make build-jar` | Build CIRCE Java JAR file and dependencies |
| `make clean` | Clean all build artifacts |
| `make help` | Show help message with all available commands |
| `make check-deps` | Check if all dependencies are available |
| `make status` | Show project status |
| `make list-tests` | List all available test files |

## 🎯 **Recommended Workflow**

### **First Time Setup**
```bash
# 1. Set up everything
make setup

# 2. Run quick test to verify
make test-quick

# 3. Run comprehensive test
make test-final
```

### **Daily Development**
```bash
# Quick verification
make test-quick

# Full validation
make test-final
```

### **CI/CD Pipeline**
```bash
# Build for CI/CD
make ci-build

# Run CI tests
make ci-test
```

## 🔧 **Troubleshooting**

### **Common Issues**

1. **Dependencies not found**
   ```bash
   make check-deps
   ```

2. **Java build issues**
   ```bash
   make clean-java
   make build-jar
   ```

3. **Python environment issues**
   ```bash
   make clean-venv
   make setup
   ```

### **Clean Commands**
```bash
# Clean Python artifacts
make clean-python

# Clean Java artifacts
make clean-java

# Clean everything including venv
make clean-all
```

## 📊 **Test Results Summary**

The Makefile provides comprehensive testing with the following results:

- ✅ **Basic Tests**: 3/3 passed
- ✅ **Final Comprehensive Test**: 24/24 passed (100% success rate)
- ✅ **Total Warnings Found**: 160+
- ✅ **Total Errors Found**: 315+
- ✅ **Validation Categories**: 6 types detected

## 🎨 **Features**

- **Colorized Output**: Easy to read with colored status messages
- **Comprehensive Help**: `make help` shows all available commands
- **Dependency Checking**: `make check-deps` verifies all requirements
- **Flexible Testing**: Multiple test levels from quick to comprehensive
- **CI/CD Ready**: Commands suitable for automated pipelines
- **Error Handling**: Graceful handling of missing files and dependencies

## 📁 **Project Structure**

```
cohort_validator/
├── Makefile                 # This makefile
├── cohort_validator.py      # Main Python interface
├── test_*.py               # Test files
├── requirements.txt        # Python dependencies
├── circe-be/              # Java library
│   ├── target/            # Built JAR files
│   └── src/               # Java source code
└── venv/                  # Python virtual environment
```

## 🚀 **Next Steps**

1. **Run the tests**: `make test-final`
2. **Validate your cohorts**: `make validate-cohort FILE=your_cohort.json`
3. **Explore the code**: Check `cohort_validator.py` for the Python API
4. **Read documentation**: See `README.md` and `TEST_SUMMARY.md`

---

**Happy validating!** 🎉
