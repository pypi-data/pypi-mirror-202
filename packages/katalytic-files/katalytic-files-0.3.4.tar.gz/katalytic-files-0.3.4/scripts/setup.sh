# # reset
source scripts/cleanup.sh
python -m venv venv
source venv/bin/activate

# install deps
pip install --upgrade $(python scripts/find_requirements.py)
pip install ../katalytic-images/

# install this pkg
if [[ $1 == 'pypi' ]]; then
	pip install $(cdir)
elif [[ $1 == 'test' ]]; then
	pip install -i https://test.pypi.org/simple/ $(cdir)
else
	pip install -e .
fi

# test
source scripts/pytest.sh
