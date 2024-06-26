.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
SERVER_IP ?= caserna.local
USERNAME ?= yoyo
export SERVER_IP
export USER

export CRYPTOGRAPHY_DONT_BUILD_RUST=1

BROWSER := python -c "$$BROWSER_PYSCRIPT"

CURRENT_VERSION = $(shell python setup.py --version)

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-all: clean ## Remove everything including .env
	rm -rf .env/
	rm -rf .tox/

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8
	flake8 caserna tests

lint: lint/flake8 ## check style

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source caserna -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/caserna.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ caserna
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

install-ega: clean dist
	scp dist/*.whl $(USERNAME)@$(SERVER_IP):~/
	ssh $(USERNAME)@$(SERVER_IP) "pip3 install ~/~/*.whl"
	ssh $(USERNAME)@$(SERVER_IP) "rm ~/~/*.whl"

env-create:  ## creates a virtual environment using tox
	tox -e caserna --recreate
	@echo -e "\r\nYou can activate the environment with:\r\n\r\n$$ source ./.tox/caserna/bin/activate\r\n"

install-requirements:  ## install requirements
	pip install -r requirements.txt

run-app: ## run the app
	python3 caserna/flask_app.py

create-grafana-storage: ## creates the grafana storage
	docker volume create grafana-storage

run-grafana: create-grafana-storage ## run the app
	docker run -d -p 3000:3000 --name=grafana -v grafana-storage:/var/lib/grafana caserna_grafana:latest

start-db: ## starts the database
	docker-compose -f docker/docker-compose.yml up -d --force-recreate

stop-db: ## stops the database
	docker-compose -f docker/docker-compose.yml down

build-grafana:
	docker build -t caserna_grafana -f docker/grafana_docker/Dockerfile .

build-caserna: clean dist
	docker build -t caserna -f docker/Dockerfile .
	rm -rf dist/
	rm -rf build/

build-all: build-grafana build-caserna

save-dockers:
	docker save caserna_grafana:latest | gzip > docker/caserna_grafana.tar.gz
	docker save caserna:latest | gzip > docker/caserna.tar.gz

send-dockers: save-dockers
	scp docker/caserna_grafana.tar.gz $(USERNAME)@$(SERVER_IP):~/
	scp docker/caserna.tar.gz $(USERNAME)@$(SERVER_IP):~/
	ssh $(USERNAME)@$(SERVER_IP) "docker load < ~/caserna_grafana.tar.gz"
	ssh $(USERNAME)@$(SERVER_IP) "docker load < ~/caserna.tar.gz"
	ssh $(USERNAME)@$(SERVER_IP) "rm ~/caserna_grafana.tar.gz"
	ssh $(USERNAME)@$(SERVER_IP) "rm ~/caserna.tar.gz"

env-compile:
	pip-compile --output-file requirements.txt requirements.in

save-caserna: build-caserna
	docker save caserna:latest | gzip > docker/caserna.tar.gz

send-caserna: save-caserna
	scp docker/caserna.tar.gz $(USERNAME)@$(SERVER_IP):~/
	ssh $(USERNAME)@$(SERVER_IP) "docker load < ~/caserna.tar.gz"

send-docker:
	scp docker/docker-compose.yml $(USERNAME)@$(SERVER_IP):~/
