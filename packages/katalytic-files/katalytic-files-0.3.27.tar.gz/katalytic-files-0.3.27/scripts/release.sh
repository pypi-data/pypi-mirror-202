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
	python -m pip install --quiet --quiet twine flit packaging
	python -m pip install --quiet --quiet python-semantic-release==7.29.0
}

check_build(){
	pkg="$1"
	twine check dist/*
	if [ $? -eq 0 ]; then
		echo "[twine] ok"
	else
		echo "[twine] Check failed. Exiting ..."
		exit 1
	fi

	python -m pip install --quiet --quiet dist/*.tar.gz
	python -c "from $pkg import __version__; print(__version__)"
	if [ $? -eq 0 ]; then
		echo "[sdist] ok"
	else
		echo "[sdist] Import failed. Exiting ..."
		exit 1
	fi

	python -m pip install --quiet --quiet dist/*-py3-none-any.whl
	python -c "from $pkg import __version__; print(__version__)"
	if [ $? -eq 0 ]; then
		echo "[wheel] ok"
	else
		echo "[wheel] Import failed. Exiting ..."
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
	git config credential.helper '!f() { printf "%s\n" "username=vali19th" "password=$GITLAB_TOKEN"; };f'
	git config pull.rebase false
	git pull --no-edit

	# bump version and update changelog
	new_version="$(semantic-release print-version)"
	if [[ "$new_version" != "" ]]; then
		$(semantic-release version)
		update_changelog "$new_version"
		command cat CHANGELOG.md
	else
		echo "No version bump. Exiting ..."
		exit 0
	fi

	flit build
	check_build "$pkg"

	# release
	flit publish --repository pypi

	# push
	git add CHANGELOG.md && git commit -m "doc: update CHANGELOG.md"
	git push --tags
	git push origin HEAD:main
}

main
