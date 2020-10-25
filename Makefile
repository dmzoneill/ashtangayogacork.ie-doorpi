help:
	@echo "This project supports the following targets"
	@echo ""
	@echo " make help - show this text"
	@echo " make lint - run flake8"
	@echo " make test - run the unittests and lint"
	@echo " make clean - remove unneeded files"
	@echo ""

lint:
	@echo "Running flake8"
	@tox -e lint

test: lint unittest

unittest:
	@tox -e unit

clean:
	@echo "Cleaning files"
	@if [ -d ./.tox ] ; then rm -rf ./.tox ; fi
	@if [ -d ./.pytest_cache ] ; then rm -rf ./.pytest_cache ; fi
	@if [ -d ./reports ] ; then rm -rf ./reports ; fi
	@if [ -f ./.coverage ] ; then rm -rf ./.coverage ; fi

# The targets below don't depend on a file
.PHONY: lint test unittest clean help