# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynpc']

package_data = \
{'': ['*'], 'pynpc': ['data/*']}

install_requires = \
['click-help-colors>=0.9.1,<0.10.0',
 'click>=8.1.3,<9.0.0',
 'orjson>=3.8.10,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=12.4.4,<14.0.0',
 'structlog>=22.1.0,<23.0.0',
 'types-requests>=2.28.11.17,<3.0.0.0']

entry_points = \
{'console_scripts': ['pynpc = pynpc.console:main']}

setup_kwargs = {
    'name': 'pynpc',
    'version': '0.1.0',
    'description': 'Generate simple NPCs for table top role playing games',
    'long_description': '# pynpc\n\n[![PyPi status](https://img.shields.io/pypi/status/Setupr)](https://img.shields.io/pypi/status/Setupr)\n[![PyPi version](https://img.shields.io/pypi/v/pynpc)](https://img.shields.io/pypi/v/pynpc)\n[![PyPi python versions](https://img.shields.io/pypi/pyversions/Setupr)](https://img.shields.io/pypi/pyversions/Setupr)\n[![PyPi downloads](https://img.shields.io/pypi/dm/pynpc)](https://img.shields.io/pypi/dm/Setupr)\n\n[![Release](https://img.shields.io/github/v/release/kierun/pynpc)](https://img.shields.io/github/v/release/kierun/pynpc)\n[![Build status](https://img.shields.io/github/actions/workflow/status/kierun/pynpc/codeql.yml?branch=main)](https://img.shields.io/github/actions/workflow/status/kierun/pynpc/codeql.yml?branch=main)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/kierun/pynpc)](https://img.shields.io/github/commit-activity/m/kierun/pynpc)\n[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)\n\n---\n\n## Documentation\n\n- [Installation](docs/installation.md)\n- [Usage](docs/usage.md)\n- [Development](docs/development.md)\n\n---\n\n## What is this?\n\nA simple NPC generator for all your table top role playing games.\n\n## Thanks\n\n- [Tarot card data taken from E Kelen](https://github.com/ekelen/tarot-api).\n',
    'author': 'Dr Yann Golanski',
    'author_email': 'github@kierun.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kierun/pynpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
