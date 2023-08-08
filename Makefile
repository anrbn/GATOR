ifeq ($(OS),Windows_NT)
    CLEAN_CMD := powershell -ExecutionPolicy Bypass -File clean.ps1
    PYTHON := py.exe
else
    CLEAN_CMD := rm -rf dist build *.egg-info
    PYTHON := python3
endif

.PHONY: clean build upload

all: clean build upload

clean:
	$(CLEAN_CMD)

build:
	$(PYTHON) setup.py sdist bdist_wheel

upload:
	twine upload dist/*
