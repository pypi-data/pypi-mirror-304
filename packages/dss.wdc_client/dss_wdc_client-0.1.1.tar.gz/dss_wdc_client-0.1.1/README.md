Step 1: After clean rebuild
=== 

	poetry install

Step 2: Typical cases
=== 

* Abhängigkeiten aktualisieren
	 poetry update
	 
* Eine Python-Datei: src/main.py

	poetry run python3 src/main.py
	
* Testfälle siehe: https://pytest-with-eric.com/getting-started/poetry-run-pytest/

	poetry run pytest 
	poetry run pytest -k test_simple
	poetry run pytest -s (mit Output)
	
Publish to PyPI
===
(https://python-poetry.org/docs/repositories/#publishable-repositories)
	
1. Config token (once)
	poetry config pypi-token.pypi <my-token>

2. Publish
	poetry publish --build

