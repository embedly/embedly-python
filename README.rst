embedly-python
==============
Python library for interacting with Embedly's API. To get started sign up for
a key at `embed.ly/signup <https://app.embed.ly/signup>`_.

Install
-------
Install with `Pip <http://www.pip-installer.org>`_ (recommended)::

  pip install embedly

Or easy_install::

  easy_install Embedly

Or setuptools::

  git clone git://github.com/embedly/embedly-python.git
  python setup.py

Setup requires Setuptools 0.7+ or Distribute 0.6.2+ in order to take advantage
of the ``2to3`` option. Setup will still run on earlier versions but you'll
see a warning and ``2to3`` won't happen. Read more in the Setuptools
`docs <http://pythonhosted.org/setuptools/python3.html>`_

Getting Started
---------------
This library is meant to be a dead simple way to interact with the Embedly API.
There are only 2 main objects, the ``Embedly`` client and the ``Url`` response
model. Here is a simple example and then we will go into the objects::

  >>> from embedly import Embedly
  >>> client = Embedly(:key)
  >>> obj = client.oembed('http://instagram.com/p/BL7ti/')
  >>> obj['type']
  u'photo'
  >>> obj['url']
  u'http://images.ak.instagram.com/media/2011/01/24/cdd759a319184cb79793506607ff5746_7.jpg'

  >>> obj = client.oembed('http://instagram.com/error/error/')
  >>> obj['error']
  True

Embedly Client
""""""""""""""
The Embedly client is a object that takes in a key and optional User Agent
and timeout parameters then handles all the interactions and HTTP requests
to Embedly. To initialize the object, you'll need the key that you got when
you signed up for Embedly.
::

  >>> from embedly import Embedly
  >>> client = Embedly('key')
  >>> client2 = Embedly('key', 'Mozilla/5.0 (compatible; example-org;)')
  >>> client3 = Embedly('key', 'Mozilla/5.0 (compatible; example-org;)', 30)
  >>> client4 = Embedly('key', timeout=10, user_agent='Mozilla/5.0 (compatible; example-org;)')

The client object now has a bunch of different methods that you can use.

``oembed``
  Corresponds to the `oEmbed endpoint
  <http://embed.ly/docs/embed/api/endpoints/1/oembed>`_. Passes back an object
  that allows you to retrieve a title, thumbnail, description and the embed
  html::

    >>> client.oembed('http://vimeo.com/18150336')
    <embedly.models.Url at 0x10223d950>

``extract``
  Corresponds to the `Extract endpoint
  <http://embed.ly/docs/extract/api/endpoints/1/extract>`_. Passes back an
  object that allows you to retrieve a title, description, content, html and a
  list of images.::

    >>> client.extract('http://vimeo.com/18150336')
    <embedly.models.Url at 0x10223d950>

``preview``
  **Preview is no longer available to new users and has been replaced by extract.**

  Corresponds to the `Preview endpoint
  <http://embed.ly/docs/endpoints/1/preview>`_. Passes back a simple object
  that allows you to retrieve a title, description, content, html and a list of
  images.::

    >>> client.preview('http://vimeo.com/18150336')
    <embedly.models.Url at 0x10223d950>

``objectify``
  **Objectify is no longer available to new users and has been replaced by extract.**

  Corresponds to the `Objectify endpoint
  <http://embed.ly/docs/endpoints/2/objectify>`_. Passes back a simple object
  that allows you to retrieve pretty much everything that Embedly knows about a
  URL.::

    >>> client.objectify('http://vimeo.com/18150336')
    <embedly.models.Url at 0x10223d950>

The above functions all take the same arguements, a URL or a list of URLs and
keyword arguments that correspond to Embedly's `query arguments
<http://embed.ly/docs/endpoints/arguments>`_. Here is an example::

  >>> client.oembed(['http://vimeo.com/18150336',
    'http://www.youtube.com/watch?v=hD7ydlyhvKs'], maxwidth=500, words=20)

There are some supporting functions that allow you to limit URLs before sending
them to Embedly. Embedly can return metadata for any URL, these just allow a
developer to only pass a subset of Embedly `providers
<http://embed.ly/providers>`_. Note that URL shorteners like bit.ly or t.co are
not supported through these regexes.

``regex``
  If you would like to only send URLs that returns embed HTML via Embedly you
  can match the URL to the regex before making the call. The matching providers
  are listed at `embed.ly/providers <http://embed.ly/providers>`_::

  >>> url = 'http://vimeo.com/18150336'
  >>> client.regex.match(url)
  <_sre.SRE_Match at 0x1017ba718>

``is_supported``
  This is a simplified version of ``regex``::

  >>> url = 'http://vimeo.com/18150336'
  >>> client.is_supported(url)
  True

Url Object
""""""""""
The ``Url`` object is basically a response dictionary returned from
one of the Embedly API endpoints.
::

  >>> response = client.oembed('http://vimeo.com/18150336', words=10)

Depending on the method you are using, the response will have different
attributes. We will go through a few, but you should read the `documentation
<http://embed.ly/docs>`_ to get the full list of data that is passed back.
::

  >>> response['type']
  u'video'
  >>> response['title']
  u'Wingsuit Basejumping - The Need 4 Speed: The Art of Flight'
  >>> response['provider_name']
  u'Vimeo'
  >>> response['width']
  1280

As you can see the ``Url`` object works like a dictionary, but it's slightly
enhanced. It will always have ``method`` and ``original_url`` attributes,
which represent the Embedly request type and the URL requested.
::

  >>> response.method
  'oembed'
  >>> response.original_url
  'http://vimeo.com/18150336'

  # useful because the response data itself may not have a URL
  # (or it could have a redirected link, querystring params, etc)
  >>> response['url']
  ...
  KeyError: 'url'

For the Preview and Objectify endpoints the sub-objects can also be accessed in
the same manner.
::

  >>> obj = client.preview('http://vimeo.com/18150336', words=10)
  >>> obj['object']['type']
  u'video'
  >>> obj['images'][0]['url']
  u'http://b.vimeocdn.com/ts/117/311/117311910_1280.jpg'

Error Handling
--------------
If there was an error processing the request, the ``Url`` object will contain
an error. For example if we use an invalid key, we will get a 401 response back
::

  >>> client = Embedly('notakey')
  >>> obj = client.preview('http://vimeo.com/18150336')
  >>> obj['error']
  True
  >>> obj['error_code']
  401

Copyright
---------
Copyright (c) 2013 Embed.ly, Inc. See LICENSE for details.
