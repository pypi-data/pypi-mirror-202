#!/usr/bin/env python

from setuptools import setup
from SenderSMTPClient import __version__, __name__

setup(
    name=__name__,
    version=__version__,
    author='Vyacheslav Anzhiganov',
    author_email='hello@anzhiganov.com',
    packages=[
        __name__,
    ],
    package_data={
    },
    scripts=[
    ],
    install_requires=[
        # 'validators',
        'requests'
    ]
)
