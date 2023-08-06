if [[ -z $1 ]]; then
	echo 'You must provide a conda env to use'
else
	_CONDA_PY=~/anaconda3/envs/$1/bin/python

	$_CONDA_PY -m pip uninstall -y katalytic-pkg
	$_CONDA_PY -m pip install --no-cache-dir /media/data/projects/active/kata/katalytic-pkg/dist/katalytic*-py3-none-any.whl
	_v1=$($_CONDA_PY -c 'from katalytic.pkg import __version__; print(f"wheel = {__version__}")')

	echo '---'
	$_CONDA_PY -m pip uninstall -y katalytic-pkg
	$_CONDA_PY -m pip install --no-cache-dir /media/data/projects/active/kata/katalytic-pkg/dist/katalytic-*tar.gz
	_v2a=$($_CONDA_PY -c 'from katalytic.pkg import __version__; print(f"sdist = {__version__}")')

	echo '---'
	$_CONDA_PY -m pip uninstall -y katalytic-pkg
	$_CONDA_PY -m pip install --no-cache-dir /media/data/projects/active/kata/katalytic-pkg/dist/katalytic_*tar.gz
	_v2b=$($_CONDA_PY -c 'from katalytic.pkg import __version__; print(f"sdist = {__version__}")')

	echo '---'
	$_CONDA_PY -m pip uninstall -y katalytic-pkg
	$_CONDA_PY -m pip install -e /media/data/projects/active/kata/katalytic-pkg/
	_v3=$($_CONDA_PY -c 'from katalytic.pkg import __version__; print(f"local = {__version__}")')

	# should cleanup, JIC
	$_CONDA_PY -m pip uninstall -y katalytic-pkg

	echo $_v1
	echo $_v2a
	echo $_v2b
	echo $_v3
fi
