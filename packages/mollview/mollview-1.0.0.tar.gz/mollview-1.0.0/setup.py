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
    'version': '1.0.0',
    'description': 'mollview is a command line tool for plotting HEALPix maps from fits files.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/mollview.svg)](https://badge.fury.io/py/mollview)\n![Tests](https://github.com/MetinSa/mollview/actions/workflows/tests.yml/badge.svg)\n---\n\n\n`mollview` is a command line tool for plotting HEALPix maps from fits files. `mollview` wraps `healpy`'s `read_map` and `mollview` functions. Most `mollview` keywords are supported (see [the documentation for mollview](https://healpy.readthedocs.io/en/latest/generated/healpy.visufunc.mollview.html) for more information).\n\n# Installation\n`pip install mollview`.\n\n# Examples\n```bash\n>>> mollview my_map.fits\n\n>>> python -m mollview my_map.fits\n```\n```bash\n>>> mollview --help                           \nUsage: mollview [OPTIONS] FILENAME\n\n  Plots a HEALPix map from the commandline given a fits file.\n\nArguments:\n  FILENAME  Name of HEALPIX fits file  [required]\n\nOptions:\n  --field INTEGER                 Column to read. 0 is I, 1 is Q, and 2 is U\n                                  [default: 0]\n  --min FLOAT                     Minimum value\n  --max FLOAT                     Maximum value\n  --norm TEXT                     Normalization method\n  --cmap TEXT                     Color map\n  --unit TEXT                     Unit\n  --title TEXT                    Title\n  --save / --no-save              Save the figure  [default: no-save]\n  --coord <TEXT TEXT>...          Coordinate system  [default: None, None]\n  --cbar / --no-cbar              Show color bar  [default: cbar]\n  --notext / --no-notext          Do not show text  [default: no-notext]\n  --xsize INTEGER                 Size of the figure  [default: 800]\n  --nest / --no-nest              Use NESTED pixel ordering  [default: no-\n                                  nest]\n  --remove-dip / --no-remove-dip  Remove the dipole  [default: no-remove-dip]\n  --gal-cut FLOAT                 Symmetric galactic cut for the\n                                  dipole/monopole fit. Removes points in\n                                  latitude range [-gal_cut, +gal_cut]\n  --remove-mono / --no-remove-mono\n                                  Remove the monopole  [default: no-remove-\n                                  mono]\n  --badcolor TEXT                 Color of bad pixels  [default: gray]\n  --help                          Show this message and exit\n```",
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
