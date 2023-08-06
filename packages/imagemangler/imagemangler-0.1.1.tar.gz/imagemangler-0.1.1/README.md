Image Mangler

Image Mangler is a command-line tool for deteriorating images iteratively with quality reduction of lossy algorithms.
Features

    Reduce image quality iteratively to produce a mangled image
    Option to automatically mangle the image across all quality steps
    Option to save all mangled images to a zip file or just the last one
    Supports JPEG compression only
    Uses Poetry for dependency management

Installation

    Clone this repository: git clone https://github.com/your_username/image-mangler.git
    Navigate to the project directory: cd image-mangler
    Install the dependencies: poetry install

Usage

vbnet

Usage: image-mangler [OPTIONS] IMAGE_PATH

  Mangle an image by deteriorating it iteratively with quality reduction of
  lossy algorithms

Arguments:
  IMAGE_PATH  Path to the image to be mangled  [required]

Options:
  --quality INTEGER  Base quality to start with (default: 70)
  --quality-step INTEGER  Quality step to reduce by (default: 2)
  --auto-mangle / --no-auto-mangle  Automatically mangle the image across all quality steps (default: False)
  --help  Show this message and exit.

Example usage:

arduino

$ image-mangler image.jpg --quality 50 --quality-step 5 --auto-mangle

Saving Mangled Images

After mangling an image, you will be prompted to save the mangled images. You can choose to save all mangled images to a zip file or just the last one. The zip file will be saved as mangled_images.zip in the current directory.
License

This project is licensed under the MIT License. See the LICENSE file for details.