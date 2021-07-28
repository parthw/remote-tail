PROJECTNAME=$(shell basename $(PWD))
COMMIT=$(shell git rev-parse --short HEAD)

# Make is verbose in Linux. Made it silent
MAKEFLAGS += --silent

## usage: make [option]
## Options:
.PHONY : help
help : Makefile
	echo "Choose a command run in $(PROJECTNAME)"
	sed -n 's/^## //p' $<
	sed -n 's/^###/ /p' $<

### pylint-agent: To pylint the Tail Agent files 
.PHONY: pylint-agent
pylint-agent:
	pylint tail-agent/*.py --exit-zero

### unittests-agent: To execute unit test cases of agent
.PHONY: unittests-agent
unittests-agent:
	python3 tail-agent/test_tail_agent.py

### pylint-cli: To pylint the Tail Cli files 
.PHONY: pylint-cli
pylint-cli:
	pylint tail-cli/*.py --exit-zero

### start-agent: To start the Tail Agent for local-testing
.PHONY: start-agent
start-agent:
	python3 tail-agent/main.py

### start-cli: To start cli for local testing
.PHONY: start-cli
start-cli:
	python3 tail-cli/main.py 127.0.0.1 tail-agent/new.txt

### install-agent: To install the agent dependencies
.PHONY: install-agent
install-agent:
	python3 -m pip install -r tail-agent/requirements.txt

### install-cli: To install cli dependencies
install-cli:
	python3 -m pip install -r tail-cli/requirements.txt
