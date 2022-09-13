<<<<<<< HEAD
.PHONY: install virtualenv ipython clean test pflake8 fmt lint watch docs docs-serve build
=======
.PHONY: install virtualenv ipython clean  test fmt lint pflake8 watch docs docs-serve build publish-test publish
>>>>>>> projeto-dundie-rewards/main


install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[test,dev]'


virtualenv:
	@python -m venv .venv


ipython:
	@.venv/bin/ipython

<<<<<<< HEAD

lint:
	#@.venv/bin/mypy --ignore-missing-imports dundie
	@.venv/bin/pflake8

fmt:
	@.venv/bin/isort --profile=black -m 3 dundie tests integration
=======
lint:
	@.venv/bin/flake8 dundie

fmt:
	@.venv/bin/isort dundie tests integration
>>>>>>> projeto-dundie-rewards/main
	@.venv/bin/black dundie tests integration

test:
	@.venv/bin/pytest -s --forked

<<<<<<< HEAD
=======
testci:
	@.venv/bin/pytest -v --junitxml=text-result.xml --forked

>>>>>>> projeto-dundie-rewards/main
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

<<<<<<< HEAD

docs:
	@mkdocs build --clean


docs-serve:
	@mkdocs serve

=======
>>>>>>> projeto-dundie-rewards/main
build:
	@python setup.py sdist bdist_wheel

publish-test:
	@twine upload --repository testpypi dist/*

publish:
	@twine upload dist/*
