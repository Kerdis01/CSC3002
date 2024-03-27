
default: yolov5

install:
	@echo "Installing environment"
	@chmod +x install.sh
	@./install.sh

yolov5:
	@echo "Cloning yolov5"
	@git clone https://github.com/Ultralytics/yolov5.git


help:

	@echo "Available targets:"
	@echo "default: yolov5"
	@echo "yolov5: Install the yolov5 repo"
	@echo "install: Install the requirements for the repo. Please set up an environment first."

.PHONY: default install help