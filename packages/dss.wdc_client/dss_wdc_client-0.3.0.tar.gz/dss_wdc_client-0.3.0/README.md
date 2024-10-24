# Step 1: After clean rebuild

	wdc-res-api-python> poetry install

# Step 2: Typical cases

* Update dependencies: `poetry update`
	 
* Execute Python file: `poetry run python3 src/main.py`
	
* Running tests 
(https://pytest-with-eric.com/getting-started/poetry-run-pytest/)

	poetry run pytest 
	poetry run pytest tests/test_module.py::testFunction
	poetry run pytest -s (mit Output)
	
# Publish to PyPI
(https://python-poetry.org/docs/repositories/#publishable-repositories)
	
1. Config token (once)
	
	poetry config pypi-token.pypi <my-token>

2. Publish

	poetry publish --build
