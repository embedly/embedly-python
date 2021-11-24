from __future__ import absolute_import, unicode_literals
from .py3_utils import python_2_unicode_compatible, IterableUserDict


@python_2_unicode_compatible
class Url(IterableUserDict, object):
    """
    A dictionary with two additional attributes for the method and url.
    UserDict provides a dictionary interface along with the regular
    dictionary accessible via the `data` attribute.

    """
    def __init__(self, data=None, method=None, original_url=None, **kwargs):
        super(Url, self).__init__(data, **kwargs)
        self.method = method or 'url'
        self.original_url = original_url

    def __str__(self):
        return '<%s %s>' % (self.method.title(), self.original_url or "")
