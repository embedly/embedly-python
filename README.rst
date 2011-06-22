embedly-python
==============
Python Library for interacting with Embedly's API. To get started sign up for
a key at `embed.ly/pricing <http://embed.ly/pricing>`_.

Install
=======
Basic install directions::

  git clone git@github.com:embedly/embedly-python
  sudo python setup.py

Getting Started
===============
Basic usage::

  >>> from embedly import Embedly
  >>> client = Embedly(:key)
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


Copyright
=========
Copyright (c) 2011 Embed.ly, Inc. See LICENSE for details.