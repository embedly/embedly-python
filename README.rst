embedly-python
==============
Python Library for interacting with Embedly's API. To get started sign up for
a key at `embed.ly/signup <http://embed.ly/signup>`_.

Install
-------
Install with `Pip <http://www.pip-installer.org>`_ (recommended)::

  pip install embedly

Or easy_install

  sudo easy_install Embedly

Or setuptools::

  git clone git://github.com/embedly/embedly-python.git
  sudo python setup.py


Getting Started
---------------
This library is meant to be a dead simple way to interact with the Embedly API.
There are only 2 main objects, the ``Embedly`` client and the ``Url`` model.
Here is a simple example and then we will go into the objects::

  >>> from embedly import Embedly
  >>> client = Embedly(:key)
  >>> obj = client.oembed('http://instagr.am/p/BL7ti/')
  >>> obj.type
  u'photo'
  >>> obj['type']
  u'photo'
  >>> obj.url
  u'http://distillery.s3.amazonaws.com/media/2011/01/24/cdd759a319184cb79793506607ff5746_7.jpg'

  >>> obj = client.oembed('http://instagr.am/p/error')
  >>> obj.error
  True

Embedly Client
""""""""""""""
The Embedly client is a object that takes in a key and an optional User Agent
then handles all the interactions and HTTP requests to Embedly. To initialize
the object pass in your key you got from signing up for Embedly and an optional
User Agent.

  >>> from embedly import Embedly
  >>> client = Embedly('key', 'Mozilla/5.0 (compatible; example-org;)')

The client object now has a bunch of different methods that you can use.

``oembed``
  Corresponds to the `oEmbed endpoint
  <http://embed.ly/docs/endpoints/1/oembed>`_. Passes back a simple object that
  allows you to retrieve a title, thumbnail, description and the embed html::

    >>> client.oembed('http://vimeo.com/18150336')
    <embedly.models.Url at 0x10223d950>

``preview``
  Corresponds to the `Preview endpoint
  <http://embed.ly/docs/endpoints/1/preview>`_. Passes back a simple object
  that allows you to retrieve a title, description, content, html and a list of
  images.::

    >>> client.preview('http://vimeo.com/18150336')
    <embedly.models.Url at 0x10223d950>

``objectify``
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

There are some supporting functions that allow you to limit urls before sending
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
The ``Url`` Object is just a smart dictionary that acts more like an object.
For example when you run ``oembed`` you get back a Url Object:

  >>> obj = client.oembed('http://vimeo.com/18150336', words=10)

Depending on the method you are using, the object has a different set of
attributes. We will go through a few, but you should read the `documentation
<http://embed.ly/docs>`_ to get the full list of data that is passed back.::

  # Url Object can be accessed like a dictionary
  >>> obj['type']
  u'video'
  # Data can also be accessed like attributes
  >> obj.type
  u'video'
  # Invalid attributes are returned as None
  >>> obj.notanattribute

  # The url object always has an ``orginal_url`` attrbiute.
  >>> obj.original_url
  u'http://vimeo.com/18150336'
  # The method used to retrive the URL is also on the obj
  >>> obj.method
  u'oembed'

For the Preview and Objectify endpoints the sub objects can also be accessed in
the same manner.

  >>> obj = client.preview('http://vimeo.com/18150336', words=10)
  >>> obj.object.type
  u'video'
  >>> obj.images[0].url
  u'http://b.vimeocdn.com/ts/117/311/117311910_1280.jpg'

Error Handling
--------------
If there was an error processing the request, The ``Url`` object will contain
an error. For example if we use an invalid key, we will get a 401 response back
::

  >>> client = Embedly('notakey')
  >>> obj = client.preview('http://vimeo.com/18150336', words=10)
  >>> obj.error
  True
  >>> obj.error_code
  401

Copyright
---------
Copyright (c) 2011 Embed.ly, Inc. See LICENSE for details.