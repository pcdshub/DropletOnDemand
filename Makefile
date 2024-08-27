SHELL:=/bin/bash
VERSION=0x03

FTPUSER ?=joshc


.PHONY: hil-get-test
hil-get-test:
	@source venv/bin/activate && pytest --capture=tee-sys -vv ./tests/HIL/get-test/

.PHONY: hil-set-test
hil-set-test:
	@source venv/bin/activate && pytest --capture=tee-sys -vv ./tests/HIL/set-test/

.PHONY: hil-do-test
hil-do-test:
	@source venv/bin/activate && pytest --capture=tee-sys -vv ./tests/HIL/do-test/

.PHONY: hil-all-test
hil-all-test:
	@source venv/bin/activate && pytest --capture=tee-sys -vv ./tests/HIL/

.PHONY: update_drops
update_drops:
	@cd drops && pip install --editable ..

.PHONY: run_test_server
run_test_server:
	@python3 tests/testServer.py

.PHONY: transfer_working_files
transfer_working_files:
	rsync -zvaP Makefile setup.py tests drops $(FTPUSER)@psbuild-rhel7:~/DoDRobotCode/

