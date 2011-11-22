from setuptools import setup

extra = {}

setup(
    name = 'Embedly',
    version = '0.3',
    author = 'Embed.ly, Inc.',
    author_email = 'support@embed.ly',
    description = 'Python lib for Embedly',
    license = """
    Copyright (c) 2011, Embed.ly, Inc.
    All rights reserved.  Released under the 3-clause BSD license.
    """,
    url = "https://github.com/embedly/embedly-python",
    packages = ['embedly'],
    install_requires = [
        'httplib2'
    ],
    zip_safe = True,
    **extra
)

