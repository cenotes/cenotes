#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "flask==0.12.2",
    "pynacl==1.1.2",
    "flask-sqlalchemy==2.3.2",
    "flask-migrate==2.1.1",
    "flask-script==2.0.6",
    "python-dateutil==2.6.1"
]

test_requirements = [
    "pytest",
    "tox",
    "pytest-flask",
    "coverage",
    "flake8"
]

setup(
    name='cenotes',
    version='0.5.1',
    description="Cryptographical Expendable Notes",
    long_description=readme + '\n\n' + history,
    author="John Paraskevopoulos",
    author_email='ioparaskev@gmail.comm',
    url='https://github.com/ioparaskev/cenotes',
    python_requires=">=3.3",
    packages=[
        'cenotes',
        'cenotes.utils'
    ],
    entry_points={
        "console_scripts": ['cenotes = cenotes.cli:main']
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='cenotes',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
