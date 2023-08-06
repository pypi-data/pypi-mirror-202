# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imagemangler', 'imagemangler.core']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'pillow>=9.5.0,<10.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['imagemangler = imagemangler.cli:app']}

setup_kwargs = {
    'name': 'imagemangler',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Image Mangler\n\nImage Mangler is a Python command-line tool for deteriorating images iteratively with quality reduction of lossy algorithms such as JPEG compression.\n',
    'author': 'miguelvalente',
    'author_email': 'miguelvalente@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
