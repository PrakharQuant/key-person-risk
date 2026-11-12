.PHONY: all install prices events study index export site test clean

all: install prices events study index export

install:
	pip install -e .[llm]

prices:
	python -m kpr.data_prices

events:
	python -m kpr.data_events

study:
	python -m kpr.event_study

index:
	python -m kpr.index

export:
	python -m kpr.export

site: export
	@echo "Site ready in docs/"

test:
	pytest -q

clean:
	rm -rf data/raw/*.parquet data/processed/* docs/data/*
