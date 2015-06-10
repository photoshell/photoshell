REBUILD_FLAG =
VENV=env
BIN=$(VENV)/bin
ACTIVATE=. $(BIN)/activate

.PHONY: all
all: test build pre-commit

.PHONY: pre-commit
pre-commit: .git/hooks/pre-commit
.git/hooks/pre-commit: .pre-commit-config.yaml $(VENV)
	$(ACTIVATE); pre-commit install

$(VENV): $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	test -d $(VENV) || virtualenv -p /usr/bin/python3 --system-site-packages $(VENV)
	$(ACTIVATE); pip install -r requirements.txt
	$(ACTIVATE); pip install -r requirements-dev.txt
	touch $(BIN)/activate


.PHONY: test
test: $(VENV)
	$(ACTIVATE); tox $(REBUILD_FLAG)

.PHONY: build
build: pre-commit

.PHONY: run
run: build $(VENV)
	$(ACTIVATE); python -m photoshell

.PHONY: debug
debug: build $(VENV)
	GTK_DEBUG=interactive $(ACTIVATE); python -m photoshell

.PHONY: clean
clean:
	find . -iname '*.pyc' | xargs rm -f
	rm -rf .tox
	rm -rf $(VENV)

.PHONY: art
art:
	$(MAKE) -C $@
