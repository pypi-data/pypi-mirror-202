import argparse
import json
import os
import re
import subprocess
import time

from pathlib import Path

RED = "\033[31m"
RESET = "\033[0m"

parser = argparse.ArgumentParser()
parser.add_argument('--wait', type=int, default=10, help='Wait time in minutes betwen releasing the package and installing it for testing')
args = parser.parse_args()


def main():
    package, version = get_package_name_and_version()
    main_prep()
    main_editable_install(package, version)
    main_build(package, version)
    main_check_sdist(package, version)
    main_check_wheel(package, version)
    main_release_test(package, version, args.wait)
    main_release(package, version, args.wait)


def main_prep():
    print(f'\n\n{RED}[release.py] Clearing out the junk ...{RESET}')
    shell('rm -rf $(find . -name \'*.egg-info\')')
    shell('rm -rf build dist')


def main_editable_install(package, version):
    print(f'\n\n{RED}[release.py] Creating editable install ...{RESET}')

    create_env('pytest pytest-cov pytest-randomly pytest-repeat')
    out = shell('venv/bin/python -m pip install -e .')
    assert f'Successfully installed {package}-{version}' in out, out

    run_pytest('.', count=1)


def main_build(package, version):
    print(f'\n\n{RED}[release.py] Building ...{RESET}')
    create_env()
    package_underscore = package.replace('-', '_')

    out = shell('venv/bin/python -m build .')
    search = f'Successfully built {package}-{version}.tar.gz and {package_underscore}-{version}-py3-none-any.whl'
    assert search in out, print(f'Searching for: {search!r}', '\n', out)

    out = shell('twine check dist/*')
    search = f'Checking dist/{package_underscore}-{version}-py3-none-any.whl:.*PASSED.*'
    assert re.search(search, out), print(f'Searching for: {search!r}', '\n', out)

    search = f'Checking dist/{package}-{version}.tar.gz:.*PASSED.*'
    assert re.search(search, out), print(f'Searching for: {search!r}', '\n', out)


def main_check_sdist(package, version):
    print(f'\n\n{RED}[release.py] Checking source distribution ...{RESET}')
    create_env()

    out = shell(f'venv/bin/python -m pip install --no-cache-dir dist/{package}-*tar.gz')
    assert f'Successfully built {package}' in out, out
    assert f'Successfully installed {package}-{version}' in out, out

    package_dot = package.replace('-', '.')
    out = shell(f'venv/bin/python -c "from {package_dot} import __version__; print(__version__)"')
    assert out == version, out


def main_check_wheel(package, version):
    print(f'\n\n{RED}[release.py] Checking wheel ...{RESET}')
    shell('rm -rf venv')
    shell('python -m venv venv')

    package_underscore = package.replace('-', '_')
    out = shell(f'venv/bin/python -m pip install --no-cache-dir dist/{package_underscore}-*-py3-none-any.whl')
    assert f'Successfully installed {package}-{version}' in out, out

    package_dot = package.replace('-', '.')
    out = shell(f'venv/bin/python -c "from {package_dot} import __version__; print(__version__)"')
    assert out == version, out


def main_release_test(package, version, wait):
    print(f'\n\n{RED}[release.py] Releasing on test.pypi.org ...{RESET}')
    create_env('pytest pytest-cov pytest-randomly pytest-repeat')

    out = shell(f'venv/bin/python -m twine upload -r testpypi dist/* --verbose')
    assert f'https://test.pypi.org/project/{package}/{version}/' in out, out

    print(f'\n\n{RED}[release.py] Waiting for {wait}m to give pypi time to update the package version ...{RESET}')
    time.sleep(wait)

    out = shell(f'venv/bin/python -m pip install -i https://test.pypi.org/simple/ --no-deps --no-cache-dir {package}=={version}')
    assert f'Successfully installed {package}-{version}' in out, out

    package_dot = package.replace('-', '.')
    out = shell(f'venv/bin/python -c "from {package_dot} import __version__; print(__version__)"')
    assert out == version, out

    run_pytest(package, count=1)


def main_release(package, version, wait):
    print(f'\n\n{RED}[release.py] Releasing on pypi.org ...{RESET}')
    create_env('pytest pytest-cov pytest-randomly pytest-repeat')

    out = shell(f'venv/bin/python -m twine upload dist/* --verbose')
    assert f'https://pypi.org/project/{package}/{version}/' in out, out

    print(f'\n\n{RED}[release.py] Waiting for {wait}m to give pypi time to update the package version ...{RESET}')
    time.sleep(wait)

    out = shell(f'venv/bin/python -m pip install --no-cache-dir {package}=={version}')
    assert f'Successfully installed {package}-{version}' in out, out

    package_dot = package.replace('-', '.')
    out = shell(f'venv/bin/python -c "from {package_dot} import __version__; print(__version__)"')
    assert out == version, out

    out = shell(f'git tag v{version} && git push origin v{version}')

    run_pytest(package, count=1)


def get_install_dir(package):
    paths = os.listdir('venv/lib')
    py_dir = [p for p in paths if p.startswith('python3.')][0]
    package = package.split('-')[0]
    return f'venv/lib/{py_dir}/site-packages/{package}'


def create_env(extra_packages=''):
    shell('rm -rf venv')
    shell('python -m venv venv')
    shell(f'venv/bin/pip install --upgrade pip build twine {extra_packages}')


def run_pytest(package, *, count):
    print(f'\n\n{RED}[release.py] Running pytest ...{RESET}')
    if not Path('venv').exists():
        create_env('pytest pytest-cov pytest-randomly pytest-repeat')

    if package == '.':
        out = shell(f'venv/bin/python -m pytest --cov=src --cov-report term-missing --count {count} -x')
    else:
        cov_dir = get_install_dir(package)
        out = shell(f'venv/bin/python -m pytest --cov={cov_dir} --cov-report term-missing --count {count} -x')

    assert 'failed' not in out, out
    missing = re.search(r'TOTAL\s+\d+\s+(\d+)', out).group(1)
    assert missing == '0', out


def get_package_name_and_version():
    text = read('pyproject.toml')
    package = re.search('(?<=name = ")[^"]+(?=")', text).group()
    version = re.search('(?<=version = ")[^"]+(?=")', text).group()
    return package, version


def shell(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    out = result.stdout.strip()
    error = result.returncode

    assert not error, out
    return out


def read(path):
    with open(path, 'r') as f:
        return f.read()


if __name__ == '__main__':
    main()
