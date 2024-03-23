# Makefile to setup the conda environment, install Python dependencies, and download TensorFlow Lite files

# Default target executed when no arguments are given to make.
default: help

# Target that sets up the conda environment.
conda:
	@echo "Installing conda..."
	@chmod +x setup/setup_conda.sh
	@./setup/setup_conda.sh

env:
	@echo "Setting up the conda env"
	@chmod +x setup/env.sh
	@./setup/env.sh

# Target to install Python dependencies.
python:
	@echo "Installing Python dependencies..."
	@chmod +x setup/install_python_deps.sh
	@./setup/install_python_deps.sh

# Target to download TensorFlow Lite files.
models:
	@echo "Downloading TensorFlow Lite files..."
	@chmod +x setup/download_tflite_files.sh
	@./setup/download_tflite_files.sh

# Help target to display available actions.
help:
	@echo "Available make targets:"
	@echo "  default                : Help."
	@echo "  conda            		: Install conda."
	@echo "  env					: Setup the Conda virtual environment"
	@echo "  python   				: Install Python dependencies."
	@echo "  models  				: Download TensorFlow Lite files."
	@echo "  help                   : Show available targets."

.PHONY: default conda env python models help
