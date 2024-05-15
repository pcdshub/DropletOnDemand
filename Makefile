SHELL:=/bin/bash
VERSION=0x03

FTPUSER ?=joshc

.PHONY: test
test:
	@source venv/bin/activate && pytest --capture=tee-sys -vv tests/Test*.py

.PHONY: update_drops
update_drops:
	@cd drops && pip install --editable ..

.PHONY: run_test_server
run_test_server:
	@python3 tests/testServer.py

.PHONY: transfer_working_files
transfer_working_files:
	rsync -zvaP tests drops $(FTPUSER)@psbuild-rhel7:~/DoDRobotCode/
