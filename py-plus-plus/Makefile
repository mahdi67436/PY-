.PHONY: install test clean run example help

install:
	pip install -e .

test:
	python -m pytest tests/ -v

test-quick:
	python -m unittest discover tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build dist *.egg-info

run-hello:
	python run.py projects/hello/src/main.pypp

run-calculator:
	python run.py projects/calculator/src/main.pypp

run-fibonacci:
	python run.py examples/fibonacci.pypp

run-basic:
	python run.py examples/basic.pypp

examples:
	@echo "Running all examples..."
	@echo "\n=== Basic Example ==="
	python run.py examples/basic.pypp
	@echo "\n=== Control Flow Example ==="
	python run.py examples/control_flow.pypp
	@echo "\n=== Math Example ==="
	python run.py examples/math.pypp
	@echo "\n=== Calculator Example ==="
	python run.py examples/calculator.pypp

help:
	@echo "py++ Makefile commands:"
	@echo ""
	@echo "  make install       Install py++ in development mode"
	@echo "  make test          Run all tests with pytest"
	@echo "  make test-quick    Run tests with unittest"
	@echo "  make clean         Remove build artifacts"
	@echo "  make run-hello     Run hello world project"
	@echo "  make run-calculator Run calculator project"
	@echo "  make run-fibonacci Run fibonacci example"
	@echo "  make run-basic     Run basic example"
	@echo "  make examples      Run all examples"
	@echo "  make help          Show this help message"
