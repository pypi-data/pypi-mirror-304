import importlib.util

def pkg_check(module: str):
    """
    check installed packages
    :return:
    """
    # TODO: Implement package check
    try:
        settings_name = 'bomiotconf'
        exists_module = importlib.util.find_spec(f'{module}.{settings_name}')
        if exists_module is not None:
            return module
        else:
            return None
    except:
        return None


def ignore_pkg() -> list:
    return ['apscheduler', 'automat', 'django', 'pyjwt', 'pyyaml', 'adrf', 'asgiref', 'async-property', 'attrs', 'autobahn', 'build', 'cachecontrol', 'certifi', 'cffi', 'charset-normalizer', 'cleo', 'colorama', 'constantly', 'crashtest', 'cryptography', 'daphne', 'dill', 'distlib', 'django-apscheduler', 'django-cors-headers', 'django-filter', 'djangorestframework', 'djangorestframework-csv', 'drf-spectacular', 'drf-spectacular-sidecar', 'dulwich', 'et-xmlfile', 'fastjsonschema', 'filelock', 'furl', 'hyperlink', 'idna', 'importlib-metadata', 'incremental', 'inflection', 'inquirerpy', 'installer', 'jaraco.classes', 'jsonschema', 'jsonschema-specifications', 'keyring', 'more-itertools', 'msgpack', 'multiprocess', 'nestd', 'numpy', 'openpyxl', 'orderedmultidict', 'orjson', 'packaging', 'pandas', 'pexpect', 'pfzy', 'pip', 'pkginfo', 'platformdirs', 'poetry', 'poetry-core', 'poetry-plugin-export', 'prompt-toolkit', 'ptyprocess', 'pyopenssl', 'pyasn1', 'pyasn1-modules', 'pycparser', 'pyproject-hooks', 'python-dateutil', 'pytz', 'pywin32-ctypes', 'rapidfuzz', 'referencing', 'requests', 'requests-toolbelt', 'robyn', 'rpds-py', 'rustimport', 'service-identity', 'setuptools', 'shellingham', 'six', 'sqlparse', 'toml', 'tomlkit', 'trove-classifiers', 'twisted', 'txaio', 'typing-extensions', 'tzdata', 'tzlocal', 'uritemplate', 'urllib3', 'virtualenv', 'watchdog', 'wcwidth', 'wheel', 'zipp', 'zope.interface', '-omiot', 'autocommand', 'backports.tarfile', 'importlib-resources', 'inflect', 'jaraco.collections', 'jaraco.context', 'jaraco.functools', 'jaraco.text', 'tomli', 'typeguard']


def ignore_cwd() -> list:
    return ['.idea', '.venv', 'dbs', 'logs', 'media', '__pycache__']

def none_return():
    return None