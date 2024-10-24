# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aldjemy']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'SQLAlchemy>=1.4']

setup_kwargs = {
    'name': 'aldjemy-cai',
    'version': '1.0',
    'description': 'SQLAlchemy for your Django models',
    'long_description': 'Character modified version of Aldjemy. Thanks to the author.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/character-tech/aldjemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
