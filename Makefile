VENV   := .venv
PYTHON := $(VENV)/bin/python
PID    := /tmp/whipmyai.pid
LOG    := /tmp/whipmyai.log

.PHONY: install start stop status logs uninstall

install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --quiet -r requirements.txt
	@echo ""
	@echo "Done. One manual step required:"
	@echo "  System Settings → Privacy & Security → Accessibility"
	@echo "  → Add your terminal app (Terminal / iTerm2 / Warp…)"
	@echo ""
	@echo "Then: make start"

start:
	@if [ -f $(PID) ] && kill -0 $$(cat $(PID)) 2>/dev/null; then \
		echo "whipmyai is already running (PID $$(cat $(PID)))"; \
	else \
		$(PYTHON) whipmyai.py >> $(LOG) 2>&1 & echo $$! > $(PID) && \
		echo "whipmyai started  |  logs: $(LOG)  |  stop: make stop"; \
	fi

stop:
	@if [ -f $(PID) ] && kill -0 $$(cat $(PID)) 2>/dev/null; then \
		kill $$(cat $(PID)) && rm -f $(PID) && echo "whipmyai stopped"; \
	else \
		rm -f $(PID) && echo "whipmyai is not running"; \
	fi

status:
	@if [ -f $(PID) ] && kill -0 $$(cat $(PID)) 2>/dev/null; then \
		echo "running (PID $$(cat $(PID)))"; \
	else \
		echo "stopped"; \
	fi

logs:
	@tail -f $(LOG)

uninstall:
	@$(MAKE) stop 2>/dev/null; true
	rm -rf $(VENV)
	rm -f $(LOG) $(PID)
	@echo "whipmyai uninstalled (project files kept)"
