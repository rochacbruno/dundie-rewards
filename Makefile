.PHONY: install virtualenv ipython clean  test fmt lint pflake8 watch docs docs-serve build publish-test publish



install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[test,dev]'


virtualenv:
	@python -m venv .venv


ipython:
	@.venv/bin/ipython

lint:
	@.venv/bin/prospector --strictness medium
	@.venv/bin/mypy --ignore-missing-imports dundie
	@.venv/bin/flake8


fmt:
	@.venv/bin/isort --profile=black -m 3 dundie tests integration


test:
	@.venv/bin/pytest -s --forked


testci:
	@.venv/bin/pytest -v --junitxml=text-result.xml --forked


watch:
	# @.venv/bin/ptw
	@ls **/*.py | entr pytest --forked


clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build


docs:
	@mkdocs build --clean


docs-serve:
	@mkdocs serve


build:
	@python setup.py sdist bdist_wheel

publish-test:
	@twine upload --repository testpypi dist/*

publish:
	@twine upload dist/*
