rm -rf build/*
venv/bin/python -m pip install --upgrade build
# poetry build
venv/bin/python -m build .
twine check dist/*
