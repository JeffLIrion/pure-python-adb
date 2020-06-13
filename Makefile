.PHONY: docs
docs:
	rm -rf docs/build/html
	@cd docs && sphinx-apidoc -f -e -o source/ ../ppadb/
	@cd docs && make html && make html

.PHONY: test
test:
	python setup.py test

.PHONY: coverage
coverage:
	coverage run --source ppadb setup.py test && coverage html && coverage report -m

.PHONY: tdd
tdd:
	coverage run --source ppadb setup.py test && coverage report -m

.PHONY: lint
lint:
	flake8 ppadb/ && pylint ppadb/ && flake8 tests/ && pylint tests/

.PHONY: alltests
alltests:
	flake8 ppadb/ && pylint ppadb/ && flake8 tests/ && pylint tests/ && coverage run --source ppadb setup.py test && coverage report -m
