# Makefile for Phenotype Library - Python Package
# This Makefile handles building Java JAR files and Python package development

# Variables
CIRCE_DIR = circe-be
TARGET_DIR = $(CIRCE_DIR)/target
JAR_FILE = $(TARGET_DIR)/circe-1.13.0-SNAPSHOT.jar
DEPS_DIR = $(TARGET_DIR)/dependencies
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
PURPLE = \033[0;35m
CYAN = \033[0;36m
NC = \033[0m # No Color

# Default target
.PHONY: help
help: ## Show this help message
	@echo "$(CYAN)Phenotype Library - Python Package$(NC)"
	@echo "$(CYAN)====================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  make setup     # Set up environment and build everything"
	@echo "  make install   # Install package in development mode"
	@echo "  make test      # Run all tests"
	@echo "  make build     # Build package distribution"

# Setup targets
.PHONY: setup
setup: venv install-deps build-jar ## Set up the complete environment (venv, dependencies, JAR files)

.PHONY: venv
venv: ## Create Python virtual environment
	@echo "$(BLUE)Creating Python virtual environment...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
		echo "$(GREEN)✓ Virtual environment created$(NC)"; \
	else \
		echo "$(YELLOW)✓ Virtual environment already exists$(NC)"; \
	fi

.PHONY: install-deps
install-deps: venv ## Install Python dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✓ Python dependencies installed$(NC)"

# Java build targets
.PHONY: clone-circe
clone-circe: ## Clone the CIRCE repository from GitHub
	@echo "$(BLUE)Cloning CIRCE repository from GitHub...$(NC)"
	@if [ ! -d "$(CIRCE_DIR)" ]; then \
		git clone https://github.com/OHDSI/circe-be.git $(CIRCE_DIR); \
		echo "$(GREEN)✓ CIRCE repository cloned$(NC)"; \
	else \
		echo "$(YELLOW)✓ CIRCE repository already exists$(NC)"; \
	fi

.PHONY: build-jar
build-jar: clone-circe ## Build the CIRCE Java JAR file and dependencies
	@echo "$(BLUE)Building CIRCE Java library...$(NC)"
	@cd $(CIRCE_DIR) && mvn clean compile package -DskipTests -Dmaven.test.skip=true
	@echo "$(BLUE)Building Java dependencies...$(NC)"
	@cd $(CIRCE_DIR) && mvn dependency:copy-dependencies -DoutputDirectory=target/dependencies
	@echo "$(GREEN)✓ CIRCE JAR file and dependencies built$(NC)"

.PHONY: check-deps
check-deps: ## Check if JAR files and dependencies exist
	@echo "$(BLUE)Checking Java dependencies...$(NC)"
	@if [ -f "$(JAR_FILE)" ]; then \
		echo "$(GREEN)✓ CIRCE JAR file exists: $(JAR_FILE)$(NC)"; \
	else \
		echo "$(RED)✗ CIRCE JAR file missing: $(JAR_FILE)$(NC)"; \
	fi
	@if [ -d "$(DEPS_DIR)" ]; then \
		JAR_COUNT=$$(ls -1 $(DEPS_DIR)/*.jar 2>/dev/null | wc -l | xargs -I {} echo "{}"); \
		echo "$(GREEN)✓ Dependencies directory exists with $$JAR_COUNT JAR files$(NC)"; \
	else \
		echo "$(RED)✗ Dependencies directory missing: $(DEPS_DIR)$(NC)"; \
	fi

# Python package targets
.PHONY: install
install: setup ## Install package in development mode
	@echo "$(BLUE)Installing package in development mode...$(NC)"
	@$(PIP) install -e .
	@echo "$(GREEN)✓ Package installed in development mode$(NC)"

.PHONY: install-dev
install-dev: setup ## Install package with development dependencies
	@echo "$(BLUE)Installing package with development dependencies...$(NC)"
	@$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✓ Package installed with development dependencies$(NC)"

.PHONY: build
build: setup ## Build package distribution
	@echo "$(BLUE)Building package distribution...$(NC)"
	@$(PYTHON) -m build
	@echo "$(GREEN)✓ Package distribution built$(NC)"

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@echo "$(GREEN)✓ Build artifacts cleaned$(NC)"

# Test targets
.PHONY: test
test: setup ## Run all test suites
	@echo "$(PURPLE)Running all test suites...$(NC)"
	@echo "$(CYAN)========================================$(NC)"
	@$(MAKE) test-basic
	@echo ""
	@$(MAKE) test-final
	@echo ""
	@$(MAKE) test-comprehensive
	@echo ""
	@echo "$(GREEN)🎉 All tests completed!$(NC)"

.PHONY: test-basic
test-basic: setup ## Run basic validation tests
	@echo "$(BLUE)Running basic validation tests...$(NC)"
	@$(PYTHON) -m pytest cohort_validator/tests/test_validator.py -v

.PHONY: test-final
test-final: setup ## Run final comprehensive tests
	@echo "$(BLUE)Running final comprehensive tests...$(NC)"
	@$(PYTHON) -m pytest cohort_validator/tests/test_final.py -v

.PHONY: test-comprehensive
test-comprehensive: setup ## Run comprehensive validation tests
	@echo "$(BLUE)Running comprehensive validation tests...$(NC)"
	@$(PYTHON) -m pytest cohort_validator/tests/test_comprehensive.py -v

.PHONY: test-quick
test-quick: setup ## Run quick basic tests only
	@echo "$(PURPLE)Running quick basic tests...$(NC)"
	@$(MAKE) test-basic

.PHONY: test-coverage
test-coverage: setup ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@$(PIP) install coverage
	@$(PYTHON) -m coverage run -m pytest cohort_validator/tests/
	@$(PYTHON) -m coverage report
	@$(PYTHON) -m coverage html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(NC)"

# Linting and formatting
.PHONY: lint
lint: setup ## Run linting checks
	@echo "$(BLUE)Running linting checks...$(NC)"
	@$(PIP) install flake8 black isort
	@$(PYTHON) -m flake8 cohort_validator/
	@echo "$(GREEN)✓ Linting completed$(NC)"

.PHONY: format
format: setup ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	@$(PIP) install black isort
	@$(PYTHON) -m black cohort_validator/
	@$(PYTHON) -m isort cohort_validator/
	@echo "$(GREEN)✓ Code formatted$(NC)"

.PHONY: type-check
type-check: setup ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(NC)"
	@$(PIP) install mypy
	@$(PYTHON) -m mypy cohort_validator/
	@echo "$(GREEN)✓ Type checking completed$(NC)"

# Clean targets
.PHONY: clean-java
clean-java: ## Clean Java build artifacts
	@echo "$(BLUE)Cleaning Java build artifacts...$(NC)"
	@if [ -d "$(CIRCE_DIR)" ]; then \
		cd $(CIRCE_DIR) && mvn clean; \
		echo "$(GREEN)✓ Java build artifacts cleaned$(NC)"; \
	else \
		echo "$(YELLOW)✓ No CIRCE directory to clean$(NC)"; \
	fi

.PHONY: clean-circe
clean-circe: ## Remove the cloned CIRCE repository
	@echo "$(BLUE)Removing CIRCE repository...$(NC)"
	@rm -rf $(CIRCE_DIR)
	@echo "$(GREEN)✓ CIRCE repository removed$(NC)"

.PHONY: clean-python
clean-python: ## Clean Python build artifacts and cache
	@echo "$(BLUE)Cleaning Python artifacts...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	@echo "$(GREEN)✓ Python artifacts cleaned$(NC)"

.PHONY: clean-venv
clean-venv: ## Remove virtual environment
	@echo "$(BLUE)Removing virtual environment...$(NC)"
	@rm -rf $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment removed$(NC)"

.PHONY: clean
clean: clean-python clean-java ## Clean all build artifacts

.PHONY: clean-all
clean-all: clean clean-venv clean-circe ## Clean everything including virtual environment and CIRCE repository
	@echo "$(GREEN)✓ Everything cleaned$(NC)"

# Documentation
.PHONY: docs
docs: setup ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	@$(PIP) install sphinx sphinx-rtd-theme
	@$(PYTHON) -m sphinx -b html docs/ docs/_build/html/
	@echo "$(GREEN)✓ Documentation generated in docs/_build/html/$(NC)"

# Development workflow
.PHONY: dev-setup
dev-setup: setup install-dev ## Complete development setup
	@echo "$(GREEN)🎉 Development environment ready!$(NC)"
	@echo "$(CYAN)You can now:$(NC)"
	@echo "  - Run tests: make test"
	@echo "  - Format code: make format"
	@echo "  - Run linting: make lint"
	@echo "  - Build package: make build"
