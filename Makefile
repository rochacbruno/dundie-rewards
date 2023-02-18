# Makefile
.PHONY: install update ipython clean test pflake8 fmt lint watch docs docs-serve build publish code-coverage

install:
	@poetry install

update:
	@poetry update

test:
	@poetry run pytest -s --forked

code-coverage:
	@poetry run pytest --cov-report html --cov . 

watch:
	#@poetry run ptw
	@ls **/*.py | entr pytest --forked

ipython:
	@poetry run ipython

lint:
	@poetry run pflake8

fmt:
	@poetry run isort dundie tests integration
	@poetry run black dundie tests integration

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
	@poetry build

publish:
	@poetry publish
