source venv/bin/activate
python -m pytest --failed-first --cov-fail-under=100 --cov=src --cov-report term-missing
