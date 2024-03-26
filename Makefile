SHELL:=/bin/bash
VERSION=0x03

.PHONY: test
test:
	@source venv/bin/activate && pytest tests/Test*.py