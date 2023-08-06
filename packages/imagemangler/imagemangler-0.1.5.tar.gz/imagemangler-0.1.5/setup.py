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
    'version': '0.1.5',
    'description': '',
    'long_description': '![logo](https://github.com/miguelvalente/imagemangler/blob/master/logo.png?raw=true)\n\n\nImage Mangler is a command-line tool to deteriorate an image iteratively using lossy algorithms.\n\n# Installation\n\nYou can install Image Mangler via pip:\n\n```bash\npip install imagemangler\n```\n\n# Usage\n\nYou can run Image Mangler by invoking the imagemangler command in the terminal, followed by the path of the image file you want to mangle:\n\n```bash\nimagemangler path/to/image.jpg\n```\n\nBy default, Image Mangler will automatically mangle the image across all quality steps with a base quality of 70 and a quality step of 2. You can specify your own values for these parameters using the optional flags:\n\n\n```bash\nimagemangler path/to/image.jpg --quality 60 --quality-step 5 --no-auto-mangle\n```\n\nFor a more details you can use `--help`:\n\n```bash\nimagemangler --help\n```\n',
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
