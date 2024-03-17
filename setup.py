import os
import sys
import codecs
from setuptools import setup

required = ['httplib2']
tests_require = []

if sys.version_info[:2] < (2, 7):
    tests_require.append('unittest2')

if sys.version_info[:2] < (3, 3):
    tests_require.append('mock')


def get_version():
    with open(os.path.join('embedly', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')

if os.path.exists("README.rst"):
    long_description = codecs.open("README.rst", "r", "utf-8").read()
else:
    long_description = "See https://github.com/embedly/embedly-python"


setup(
    name='Embedly',
    version=get_version(),
    author='Embed.ly, Inc.',
    author_email='support@embed.ly',
    description='Python Library for Embedly',
    long_description=long_description,
    license="""
    Copyright (c) 2011, Embed.ly, Inc.
    All rights reserved.  Released under the 3-clause BSD license.
    """,
    url="https://github.com/embedly/embedly-python",
    packages=['embedly'],
    install_requires=required,
    tests_require=tests_require,
    test_suite="embedly.tests",
    zip_safe=True,
    use_2to3=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ]
)
