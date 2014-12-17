REBUILD_FLAG =
VENV=venv
BIN=$(VENV)/bin
ACTIVATE=source $(BIN)/activate

.PHONY: all
all: test build

.PHONY: pre-commit
pre-commit: .git/hooks/pre-commit
.git/hooks/pre-commit: .pre-commit-config.yaml
	pre-commit install

$(VENV): $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	test -d $(VENV) || virtualenv --system-site-packages $(VENV)
	$(ACTIVATE); pip install -r requirements.txt
	$(ACTIVATE); pip install -r requirements-dev.txt
	touch $(BIN)/activate


.PHONY: test
test: $(VENV)
	$(ACTIVATE); tox $(REBUILD_FLAG)

.PHONY: build
build: .git/hooks/pre-commit

.PHONY: clean
clean:
	find . -iname '*.pyc' | xargs rm -f
	rm -rf .tox
