#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = [x for x in f.read().splitlines() if not x.startswith(('--', '#'))]

test_requirements = ['pytest>=3', ]

setup(
    author="Greg Rabago",
    author_email='greg.rabago@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="F.R.E.D master script and modules. Idea is to contain all original apps into one for convenience. All setup is also included with commands",
    entry_points={
        'console_scripts': [
            'caserna=caserna.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='caserna',
    name='caserna',
    packages=find_packages(include=['caserna', 'caserna.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Greg0109/caserna',
    version='0.3.102',
    zip_safe=False,
)
