from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name ='p4cw',
    version = '0.1.0',
    author = 'Janne Hellsten',
    author_email = 'jjhellst@gmail.com',
    url = 'https://github.com/nurpax/p4cw',
    description = 'Perforce `p4` command line helper tool.',
    long_description = long_description,
    long_description_content_type ="text/markdown",
    license = 'MIT',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'p4cw = p4cw.p4cw:main'
        ]
    },
    classifiers =(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords ='perforce cli',
    zip_safe = False
)
