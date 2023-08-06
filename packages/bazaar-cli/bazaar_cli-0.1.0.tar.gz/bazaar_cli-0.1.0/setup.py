# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bazaar_cli']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'pyzipper>=0.3.6,<0.4.0',
 'requests>=2.28.2,<3.0.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['bazaar = bazaar_cli.main:main',
                     'bazaar-cli = bazaar_cli.main:main',
                     'bz = bazaar_cli.main:main']}

setup_kwargs = {
    'name': 'bazaar-cli',
    'version': '0.1.0',
    'description': 'Command line tool to list and download Malware Bazaar samples',
    'long_description': '',
    'author': 'matteyeux',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/matteyeux/bazaar-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
