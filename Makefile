.PHONY: install virtualenv ipython clean test pflake8 fmt lint watch docs docs-serve build


install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[test,dev]'


virtualenv:
	@python -m venv .venv


ipython:
	@.venv/bin/ipython


lint:
	#@.venv/bin/mypy --ignore-missing-imports dundie
	@.venv/bin/pflake8

fmt:
	@.venv/bin/isort --profile=black -m 3 dundie tests integration
	@.venv/bin/black dundie tests integration

test:
	@.venv/bin/pytest -s --forked

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
