if [[ -z $1 ]]; then
	echo 'You must provide a conda env to use as base for the venv'
else
	_CONDA_PY=~/anaconda3/envs/$1/bin/python

	command rm -rf venv venv
	$_CONDA_PY -m venv venv
	venv/bin/python -m pip install --upgrade pip
	venv/bin/python -m pip install --no-cache-dir /media/data/projects/active/katalytic/katalytic-pkg/dist/katalytic*-py3-none-any.whl
	_v1=$(venv/bin/python -c 'from katalytic.pkg import __version__; print(f"wheel = {__version__}")')


	_v2a="sdist A: not found"
	if [ -e /media/data/projects/active/katalytic/katalytic-pkg/dist/katalytic-*tar.gz ]; then
		command rm -rf venv venv
		$_CONDA_PY -m venv venv
		venv/bin/python -m pip install --upgrade pip
		venv/bin/python -m pip install --no-cache-dir /media/data/projects/active/katalytic/katalytic-pkg/dist/katalytic-*tar.gz
		_v2a=$(venv/bin/python -c 'from katalytic.pkg import __version__; print(f"sdist = {__version__}")')
	fi

	_v2b="sdist B: not found"
	if [ -e /media/data/projects/active/katalytic/katalytic-pkg/dist/katalytic_*tar.gz ]; then
		command rm -rf venv venv
		$_CONDA_PY -m venv venv
		venv/bin/python -m pip install --upgrade pip
		venv/bin/python -m pip install --no-cache-dir /media/data/projects/active/katalytic/katalytic-pkg/dist/katalytic_*tar.gz
		_v2b=$(venv/bin/python -c 'from katalytic.pkg import __version__; print(f"sdist = {__version__}")')
	fi


	command rm -rf venv venv
	$_CONDA_PY -m venv venv
	venv/bin/python -m pip install --upgrade pip
	venv/bin/python -m pip install -e /media/data/projects/active/katalytic/katalytic-pkg/
	_v3=$(venv/bin/python -c 'from katalytic.pkg import __version__; print(f"local = {__version__}")')

	echo $_v1
	echo $_v2a
	echo $_v2b
	echo $_v3
fi
