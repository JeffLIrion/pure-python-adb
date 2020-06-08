.PHONY: docs
docs:
	rm -rf docs/build/html
	@cd docs && sphinx-apidoc -f -e -o source/ ../aio_ppadb/
	@cd docs && make html && make html

.PHONY: test
test:
	python setup.py test

.PHONY: coverage
coverage:
	coverage run --source aio_ppadb setup.py test && coverage html && coverage report -m

.PHONY: tdd
tdd:
	coverage run --source aio_ppadb setup.py test && coverage report -m

.PHONY: lint
lint:
	flake8 aio_ppadb/ && pylint aio_ppadb/ && flake8 tests/ && pylint tests/

.PHONY: alltests
alltests:
	flake8 aio_ppadb/ && pylint aio_ppadb/ && flake8 tests/ && pylint tests/ && coverage run --source aio_ppadb setup.py test && coverage report -m
