# Makefile to setup the conda environment and install Python dependencies

# Default target executed when no arguments are given to make.
default: install

# Target that sets up the conda environment and installs dependencies.
install: setup_conda 
#install_python_deps

# Target to execute the environment setup script.
setup_conda:
	@echo "Setting up the conda environment..."
	@chmod +x setup/install.sh
	@./setup/install.sh
	@conda init
	@conda activate tflite_env

# # Target to install Python dependencies using setup.py.
# install_python_deps:
# 	@echo "Installing Python dependencies..."
# 	@python setup.py

# Help target to display available actions.
help:
	@echo "Available make targets:"
	@echo "  install            : Set up the conda environment and install Python dependencies."
	@echo "  setup_conda        : Only set up the conda environment using the install.sh script."
	@echo "  help               : Show available targets."

.PHONY: default install setup_conda help
