#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [
    "flask>=0.12.2",
    "pynacl>=1.2.0",
    "cenotes-lib>=0.2.0",
    "flask-sqlalchemy==2.3.2",
    "flask-migrate==2.1.1",
    "flask-script==2.0.6",
    "python-dateutil>=2.6.1"
]

setup_requirements = [
    "pytest-runner"
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
    version='0.8.1',
    description="Cryptographical Expendable Notes",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="John Paraskevopoulos",
    author_email='ioparaskev@gmail.comm',
    url='https://github.com/cenotes/cenotes',
    python_requires=">=3.4",
    packages=find_packages(exclude=['docs']),
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    setup_requires=setup_requirements,
    tests_require=test_requirements
)
