from setuptools import find_packages, setup
from src.aish import PACKAGE_NAME, VERSION


# Metadata
DESCRIPTION = ""
URL = ""
AUTHOR = "Zach Morris"
AUTHOR_EMAIL = "zacharymorr@outlook.com"

# Package Data
REQUIRED_PYTHON = ">=3.7"

PACKAGE_DIR = {"": "src"}

PACKAGES = find_packages(where="src")

PACKAGE_DATA = {
}

DEPENDENCIES = [
    "openai",
    "click",
]

CONSOLE_SCRIPTS = [
    f"{PACKAGE_NAME}={PACKAGE_NAME}.__main__:main",
]

# Run Setup
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    package_data=PACKAGE_DATA,
    python_requires=REQUIRED_PYTHON,
    install_requires=DEPENDENCIES,
    entry_points={"console_scripts": CONSOLE_SCRIPTS},
)
