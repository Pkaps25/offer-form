# Makefile for building a standalone executable using PyInstaller

# Define the Python interpreter and PyInstaller command
PYTHON = python
PYINSTALLER = pyinstaller

# Input Python script
BASE = fill_form
INPUT_SCRIPT = $(BASE).py

# Output directory for the standalone executable
OUTPUT_DIR = dist

# Target architecture
TARGET_ARCH = x86_64

# PyInstaller options
PYINSTALLER_OPTIONS = --onefile --target-arch $(TARGET_ARCH)

# Default target: build the standalone executable
all: build

# Build the standalone executable
build:
	$(PYINSTALLER) $(PYINSTALLER_OPTIONS) $(INPUT_SCRIPT)

# Clean generated files
clean:
	rm -rf $(OUTPUT_DIR)
	rm -rf __pycache__
	rm -rf build
	rm -rf $(BASE).spec

# Run the standalone executable
run:
	$(OUTPUT_DIR)/$(INPUT_SCRIPT:.py=)

# Phony targets
.PHONY: all build clean run
