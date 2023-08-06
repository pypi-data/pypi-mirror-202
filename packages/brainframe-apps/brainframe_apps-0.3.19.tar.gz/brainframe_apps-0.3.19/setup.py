# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brainframe_apps']

package_data = \
{'': ['*'], 'brainframe_apps': ['translations/*']}

install_requires = \
['brainframe-api>=0.29.1,<0.30.0']

entry_points = \
{'console_scripts': ['brainframe-apps = brainframe_apps.cli:cli_main']}

setup_kwargs = {
    'name': 'brainframe-apps',
    'version': '0.3.19',
    'description': 'BrainFrame Apps use BrainFrame REST API to interact with the BrainFrame OS',
    'long_description': 'None',
    'author': 'Stephen Li',
    'author_email': 'stephen@dilililabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
