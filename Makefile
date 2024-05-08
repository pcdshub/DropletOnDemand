SHELL:=/bin/bash
VERSION=0x03

.PHONY: test
test:
	@source venv/bin/activate && pytest tests/Test*.py

.PHONY: update_drops
update_drops:
	@cd drops && pip install --editable ..

.PHONY: run_test_server
run_test_server:
	@python3 tests/testServer.py
