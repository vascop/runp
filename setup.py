#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

long_description = readme

setup(
    name='runp',
    version='0.0.2',
    description='runp exports Python functions from files to the command line',
    long_description=long_description,
    author='Vasco Pinho',
    author_email='vascogpinho@gmail.com',
    url='https://github.com/vascop/runp',
    packages=find_packages(),
    test_suite='tests',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'runp = runp.runp:main',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
)
