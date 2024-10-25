import pathlib
import sys
import os
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf-8")

PKG = "preserva-tweet"

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python -m build')
    os.system('twine upload dist/*')
    sys.exit()


# This call to setup() does all the work
setup(
    name=PKG,
    version="0.5.0",
    description="Python module for ingesting Twitter exports into Preservica",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/carj/preserva-tweet",
    author="James Carr",
    author_email="drjamescarr@gmail.com",
    license="Apache License 2.0",
    packages=["preserva-tweet"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving",
    ],
    keywords='Preservica API Preservation Twitter',
    install_requires=["pyPreservica", "python-dateutil"],
    project_urls={
        'Documentation': 'https://github.com/carj/preserva-tweet',
        'Source': 'https://github.com/carj/preserva-tweet',
        'Discussion Forum': 'https://github.com/carj/preserva-tweet',
    }
)
