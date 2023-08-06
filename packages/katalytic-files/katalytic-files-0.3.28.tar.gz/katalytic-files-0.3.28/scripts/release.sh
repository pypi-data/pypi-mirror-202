prepend(){
	file="$1"
	text="$2"
	echo "$text"
	echo "$2" | command cat - "$1" > "$1.tmp" && command mv "$1.tmp" "$1"
}

update_changelog(){
	new_version="$1"
	if [[ ! -f "CHANGELOG.md" ]]; then
		touch CHANGELOG.md
	fi

	prepend CHANGELOG.md ""
	prepend CHANGELOG.md ""
	prepend CHANGELOG.md "$(semantic-release changelog)" > /dev/null
	prepend CHANGELOG.md "## $new_version ($(date +%Y-%m-%d))" > /dev/null
}

create_env(){
	if [[ $VIRTUAL_ENV ]]; then
		deactivate
	fi

	command rm -rf **/*.egg-info
	command rm -rf **/__pycache__
	command rm -rf **/.pytest_cache
	command rm -rf **/venv

	pip install --upgrade pip
	pip install twine flit packaging
	pip install python-semantic-release==7.29.0
}

check_build(){
	pkg="$1"

	twine check dist/*
	if [ $? -eq 0 ]; then
		echo "[twine] ok"
	else
		echo "[twine] Check failed. Exiting ..."
		sleep 2
		exit 1
	fi

	pip install dist/*.tar.gz
	python -c "from $pkg import __version__; print(__version__)"
	if [ $? -eq 0 ]; then
		echo "[sdist] ok"
	else
		echo "[sdist] Import failed. Exiting ..."
		sleep 2
		exit 1
	fi

	pip install --force-reinstall dist/*-py3-none-any.whl
	python -c "from $pkg import __version__; print(__version__)"
	if [ $? -eq 0 ]; then
		echo "[wheel] ok"
	else
		echo "[wheel] Import failed. Exiting ..."
		sleep 2
		exit 1
	fi
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
" )

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

	# git config and pull
	export GIT_MERGE_AUTOEDIT=no
	git config credential.helper "!f() { printf '%s\n' 'username=vali19th' 'password=$GITLAB_TOKEN'; };f"
	git config pull.rebase false
	git pull --no-edit

	# bump version and update changelog
	new_version="$(semantic-release print-version)"
	if [[ "$new_version" != "" ]]; then
		semantic-release version
		update_changelog "$new_version"
		command cat CHANGELOG.md
	else
		echo "No version bump. Exiting ..."
		sleep 2
		exit 0
	fi

	# without this, flit won't build the sdist
	git update-index --assume-unchanged pyproject.toml
	git update-index --assume-unchanged CHANGELOG.md

	flit build --format sdist --setup-py
	flit build --format wheel --setup-py
	check_build "$pkg"

	# release
	flit publish --repository pypi

	# push
	git update-index --no-assume-unchanged pyproject.toml
	git update-index --no-assume-unchanged CHANGELOG.md
	git add CHANGELOG.md && git commit -m "doc: update CHANGELOG.md"
	git push --tags
	git push origin HEAD:main
}

main
