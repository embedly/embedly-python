embedly-python
==============
Python Library for interacting with Embedly's API and Embedly Pro.

WARNING: This is alpha code. Expect it to change before a 0.1 is released.

Install
=======
Basic install directions::

  git clone git@github.com:embedly/embedly-python
  sudo python setup.py

Getting Started
===============
Basic usage::

  >>> from embedly import Embedly
  >>> client = Embedly()
  >>> obj = client.oembed('http://instagr.am/p/BL7ti/')
  >>> obj.type
  u'photo'
  >>> obj['type']
  u['photo']
  >>> obj.url
  u'http://distillery.s3.amazonaws.com/media/2011/01/24/cdd759a319184cb79793506607ff5746_7.jpg'

  >>> obj = client.oembed('http://instagr.am/p/error')
  >>> obj.error
  True

Testing
=======
The easiest way to run the test suite is with nose.

  pip install nose
  nosetests

If freshen is installed, you can also run the features.  You'll need libyaml
dev libs to install freshen successfully.

  pip install freshen
  nosetests --with-freshen

If there is some problem, it's easiest to debug by adding some options.

  nosetests --with-freshen -v -s

Copyright
=========
Copyright (c) 2011 Embed.ly, Inc. See LICENSE for details.