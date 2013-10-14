#!/usr/bin/env python
"""subdl setup file"""

requirements = []

with open('README.md') as text:
    long_description = text.read()

try:
    from setuptools import setup, find_packages
except ImportError:
    requirements.append('setuptools')
try:
    import BeautifulSoup
except ImportError:
    requirements.append('BeautifulSoup')
try:
    import requests
except ImportError:
    requirements.append('requests')

setup(name = 'subdl',
    version = '1.0.2',
    description = "a subtitle downloader for your movies and tv-series",
    long_description = long_description,
    platforms = ["Linux"],
    author = "dhirajt",
    author_email = "dhirajthakur92@facebook.com",
    url = "https://github.com/dhirajt/subdl",
    license = "GPLv3",
    packages = find_packages(),
    install_requires = requirements,
    dependency_links = ['https://pypi.python.org/pypi/requests/1.2.3',
                        'https://pypi.python.org/pypi/BeautifulSoup/3.2.1',
                        'https://pypi.python.org/pypi/setuptools/0.6c11'
],
    include_package_data = True,
    scripts = ['subdl'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
]
    )