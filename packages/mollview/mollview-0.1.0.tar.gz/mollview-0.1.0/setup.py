# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mollview']

package_data = \
{'': ['*']}

install_requires = \
['healpy>=1.16.2,<2.0.0', 'matplotlib>=3.7.1,<4.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['mollview = mollview:app']}

setup_kwargs = {
    'name': 'mollview',
    'version': '0.1.0',
    'description': 'Plot HEALPix maps from the commandline.',
    'long_description': None,
    'author': 'Metin San',
    'author_email': 'metinisan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
