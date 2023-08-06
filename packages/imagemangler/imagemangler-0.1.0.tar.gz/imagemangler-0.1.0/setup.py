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

setup_kwargs = {
    'name': 'imagemangler',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Image Mangler\n\nImage Mangler is a command-line tool for deteriorating images iteratively with quality reduction of lossy algorithms.\nFeatures\n\n    Reduce image quality iteratively to produce a mangled image\n    Option to automatically mangle the image across all quality steps\n    Option to save all mangled images to a zip file or just the last one\n    Supports JPEG compression only\n    Uses Poetry for dependency management\n\nInstallation\n\n    Clone this repository: git clone https://github.com/your_username/image-mangler.git\n    Navigate to the project directory: cd image-mangler\n    Install the dependencies: poetry install\n\nUsage\n\nvbnet\n\nUsage: image-mangler [OPTIONS] IMAGE_PATH\n\n  Mangle an image by deteriorating it iteratively with quality reduction of\n  lossy algorithms\n\nArguments:\n  IMAGE_PATH  Path to the image to be mangled  [required]\n\nOptions:\n  --quality INTEGER  Base quality to start with (default: 70)\n  --quality-step INTEGER  Quality step to reduce by (default: 2)\n  --auto-mangle / --no-auto-mangle  Automatically mangle the image across all quality steps (default: False)\n  --help  Show this message and exit.\n\nExample usage:\n\narduino\n\n$ image-mangler image.jpg --quality 50 --quality-step 5 --auto-mangle\n\nSaving Mangled Images\n\nAfter mangling an image, you will be prompted to save the mangled images. You can choose to save all mangled images to a zip file or just the last one. The zip file will be saved as mangled_images.zip in the current directory.\nLicense\n\nThis project is licensed under the MIT License. See the LICENSE file for details.',
    'author': 'miguelvalente',
    'author_email': 'miguelvalente@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
