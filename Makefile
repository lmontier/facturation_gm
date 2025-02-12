SHELL:=/bin/bash

install:
	uv venv -p 3.13
	source .venv/bin/activate && uv sync
	uv run pre-commit install

start:
	uv run streamlit run st_demo.py

generate-requirements:
	uv export --no-hashes --format requirements-txt > requirements.txt
