SHELL:=/bin/bash
VERSION=0x03

.PHONY: test
test:
	@source venv/bin/activate && pytest tests/Test*.py

.PHONY: update_drops
update_drops:
	@cd beams && pip install --editable ..
