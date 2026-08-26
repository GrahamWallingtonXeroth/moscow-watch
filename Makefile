.PHONY: check doctor test lint collect backfill tracker diff charts all

check:
	PYTHONPATH=src python3 -m moscow_watch check-config

doctor:
	PYTHONPATH=src python3 -m moscow_watch doctor --check-robots

lint:
	ruff check src tests

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

collect:
	PYTHONPATH=src python3 -m moscow_watch collect --allow-partial

backfill:
	PYTHONPATH=src python3 -m moscow_watch backfill --trades

tracker:
	PYTHONPATH=src python3 -m moscow_watch tracker

diff:
	PYTHONPATH=src python3 -m moscow_watch diff

charts:
	PYTHONPATH=src python3 -m moscow_watch charts

all: check lint test collect tracker diff charts
