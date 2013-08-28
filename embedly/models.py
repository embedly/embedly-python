from __future__ import unicode_literals

try:
    from UserDict import IterableUserDict
except ImportError:
    from collections import UserDict as IterableUserDict

class Url(IterableUserDict, object):
    """
    A dictionary with two additional attributes for the method and url.
    UserDict provides a dictionary interface along with the regular
    dictionary accsesible via the `data` attribute.

    """
    def __init__(self, data=None, method=None, original_url=None, **kwargs):
        super(Url, self).__init__(data, **kwargs)
        self.method = method or 'url'
        self.original_url = original_url

    def __str__(self):
        return self.__unicode__().encode("utf-8")

    def __unicode__(self):
        return '<%s %s>' % (self.method.title(), self.original_url or "")

    def __getitem__(self, key):
      if (key in self.data) and (self.data[key] == None):
        return ''
      else:
        return self.data[key]
