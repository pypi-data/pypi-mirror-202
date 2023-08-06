assert(){
	if [[ "$1" != "$2" ]]; then
		echo "Expected '$2'"
		echo "Got '$1'"
		if [[ "$3" ]]; then
			echo "${@:3}"
		fi
		exit 1
	fi
}

create_env(){
	if [[ $VIRTUAL_ENV ]]; then
		deactivate
	fi

	command rm -rf **/*.egg-info
	command rm -rf **/__pycache__
	command rm -rf **/.pytest_cache
	command rm -rf **/venv

	python -m venv venv
	source venv/bin/activate
}

create_pypirc(){
	  message=$(echo "
[distutils]
index-servers =
  pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = $TWINE_PASSWORD


[gitlab]
repository = https://gitlab.com/api/v4/projects/<project-id>/packages/pypi/
username = gitlab-ci-token
password =
" | sed -e 's/^[[:blank:]]{4}//' -e 's/[[:blank:]]*$//')

	echo "$message" > ~/.pypirc
	chmod 666 ~/.pypirc
}

main(){
	current_version=$(grep -P 'version = (.*)' pyproject.toml | grep -Po '[.0-9]+')
	pkg=$(grep -P 'name = (.*)' pyproject.toml | head -n 1 | grep -Po 'katalytic[-.a-z]*' | sed 's/-/./' )
	echo "Package: '$pkg'"
	echo "Current: '$current_version'"
	echo ""

	rm -rf **/dist
	rm -rf **/build
	create_pypirc

	create_env
	python -m pip install --quiet --quiet twine flit packaging
	pip install --quiet --quiet python-semantic-release==7.29.0

	# bump -> build -> check
	semantic-release version
	flit build
	twine check dist/*
	if [ $? -ne 0 ]; then
		echo "twine check failed, exiting."
		exit 1
	fi

	# release -> push
	flit publish --repository pypi
	git push --tags
}

main
