wait_until_pypi_is_ready(){
	pkg="$1"
	expected_version="$2"
	pypi="$3"
	waiting=120

	while true; do
		sleep $waiting
		response=$(curl -s https://$pypi/pypi/$pkg/json)
		if echo "${response}" | jq ".releases | has(\"$version\")" | grep -q true; then
			echo "$pkg==$version is available on $pypi!"
			break
		fi
		echo "$pkg==$version is unavailable on $pypi. Waiting $waiting seconds..."
	done
}

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

get_version(){
	python -c "from $1 import __version__; print(__version__)"
}

main_build(){
	command rm -rf **/dist
	command rm -rf **/build

	create_env
	python -m pip install --quiet --quiet flit
	flit build
}

main_check_sdist(){
	pkg="$1"
	expected_version="$2"
	create_env
	python -m pip install --quiet --quiet dist/katalytic-files*.tar.gz

	echo "[sdist] Checking ..."
	v=$(get_version "$pkg")
	assert "$v" "$expected_version" "The the installed version doesn't match the pyproject.toml one"
	echo "[sdist] OK: $v"
	echo ""
}

main_check_wheel(){
	pkg="$1"
	expected_version="$2"
	create_env
	python -m pip install --quiet --quiet dist/katalytic_files-*-py3-none-any.whl

	echo "[wheel] Checking ..."
	v=$(get_version "$pkg")
	assert "$v" "$expected_version" "The the installed version doesn't match the pyproject.toml one"
	echo "[wheel] OK: $v"
	echo ""
}

main_release_test(){
	pkg="$1"
	expected_version="$2"
	create_env
	python -m pip install --quiet --quiet twine flit

	flit publish --repository testpypi

	echo "[$pypi] waiting until the new version is available ..."
	wait_until_pypi_is_ready "$pkg" "$expected_version" "test.pypi.org"

	echo "[$pypi] Installing ..."
	python -m pip install --quiet --quiet --index-url https://test.pypi.org/simple/ $pkg==$expected_version

	echo "[$pypi] Checking ..."
	v=$(get_version "$pkg")
	assert "$v" "$expected_version" "The the installed version doesn't match the pyproject.toml one"
	echo "[$pypi] OK: $v"
	echo ""
}

main_release(){
	pkg="$1"
	expected_version="$2"
	create_env
	python -m pip install --quiet --quiet twine flit

	flit publish --repository pypi

	echo "[$pypi] waiting until the new version is available ..."
	wait_until_pypi_is_ready "$pkg" "$expected_version" "test.pypi.org"

	echo "[$pypi] Installing ..."
	python -m pip install --quiet --quiet $pkg==$expected_version

	echo "[$pypi] Checking ..."
	v=$(get_version "$pkg")
	assert "$v" "$expected_version" "The the installed version doesn't match the pyproject.toml one"
	echo "[$pypi] OK: $v"
}

main_create_pypirc(){
  message=$(echo "
    [distutils]
    index-servers =
      pypi

    [pypi]
    repository = https://upload.pypi.org/legacy/
    username = __token__
    password = $TWINE_PASSWORD
  " | sed -e 's/^[[:blank:]]{4}//' -e 's/[[:blank:]]*$//')

  echo "$message" > ~/.pypirc
  chmod 666 ~/.pypirc
}

main(){
	pkg=$(grep -P 'name = (.*)' pyproject.toml | head -n 1 | grep -Po 'katalytic[-.a-z]*' | sed 's/-/./' )
	expected_version=$(grep -P 'version = (.*)' pyproject.toml | grep -Po '[.0-9]+')
	echo "Package: '$pkg'"
	echo "Version: '$expected_version'"
	echo ""

	# build -> check stdist and wheel
	main_build
	main_check_sdist "$pkg" "$expected_version"
	main_check_wheel "$pkg" "$expected_version"

	# bump version and create changelogs
	pip install --quiet --quiet python-semantic-release==7.29.0
	expected_version=$(semantic-release version | awk '{print $NF}')

	# release
	main_create_pypirc
	# main_release_test "$pkg" "$expected_version"
	main_release "$pkg" "$expected_version"
}

main
