##
# k8s-secretgen
#
# @file
# @version 0.1

.PHONY: install devinstall test help

# target: help - Display callable targets.
help:
	@sed -n 's/^# target: \(.*\)/make \1/p' Makefile

# target: install - Install k8s-secretgen.
install:
	@pip3 install .

# target: devinstall - Install k8s-secretgen in develop mode.
devinstall:
	@pip3 install -e .

# lint - Run code linters.
lint:
	@flake8

# end
