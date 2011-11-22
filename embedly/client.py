"""
Client
======

The embedly object that interacts with the service
"""
import re
import urllib
import httplib2
import json
import itertools

from models import Url

USER_AGENT = 'Mozilla/5.0 (compatible; embedly-python/0.3;)'

class Embedly(object):
    """
    Client

    """
    def __init__(self, key=None, user_agent=USER_AGENT):
        """
        Initialize the Embedly client

        :param user_agent: User Agent passed to Embedly
        :type user_agent: str
        :param key: Embedly Pro key
        :type key: str

        :returns: None
        """        
        self.user_agent = user_agent
        self.key = key
        self.services = []
        
        self._regex = None

    def get_services(self):
        """
        get_services makes call to services end point of api.embed.ly to fetch
        the list of supported providers and their regexes
        """

        if self.services: return self.services

        url = 'http://api.embed.ly/1/services/python'

        http = httplib2.Http()
        headers = {'User-Agent' : self.user_agent}
        resp, content = http.request(url, headers=headers)

        if resp['status'] == '200':
            resp_data = json.loads(content)
            self.services = resp_data

            #build the regex that we can use later.
            _regex = []
            for each in self.get_services():
                _regex.append('|'.join(each.get('regex',[])))
    
            self._regex = re.compile('|'.join(_regex))

        return self.services

    def service_matcher(self):
        """
        Generate a really big regular expression that we can use to determine if a URL is serviced by embedly or not.
        Returns a compiled regular expression.
        """
        if self.service_re is not None:
            return self.service_re

        services            = self.get_services()
        service_expressions = list(itertools.chain.from_iterable([service['regex'] for service in services]))
        self.service_re     = re.compile('|'.join(service_expressions), re.I)

        return self.service_re

    def url_is_serviced(self, url):
        """
        If a URL is serviced by Embed.ly, return True. Otherwise return False.
        """
        return self.service_matcher().match(url) is not None

    @property
    def regex(self):
        """
        regex method just so we can raise a ValueError if needed.
        """
        if not self._regex:
            raise ValueError('get_services need to be called first.')

        return self._regex

    def _get(self, version, method, url_or_urls, **kwargs):
        """
        _get makes the actual call to api.embed.ly
        """
        if not url_or_urls:
            raise ValueError('%s requires a url or a list of urls given: %s' %
                             (method.title(), url_or_urls))

        #A flag we can use instead of calling isinstance all the time.
        multi = isinstance(url_or_urls, list)

        query = ''

        key = kwargs.get('key', self.key)

        #make sure that a key was set on the client or passed in.
        if not key:
            raise ValueError('Requires a key. None given: %s' % (key))

        kwargs['key'] = key

        query += urllib.urlencode(kwargs)
    
        if multi:
            query += '&urls=%s&' % ','.join([urllib.quote(url) for url in url_or_urls])
        else:
            query += '&url=%s' % urllib.quote(url_or_urls)

        url = 'http://api.embed.ly/%s/%s?%s' % (version, method, query)

        http = httplib2.Http()

        headers = {'User-Agent' : self.user_agent}

        resp, content = http.request(url, headers=headers)

        if resp['status'] == '200':
            data = json.loads(content)
        else:
            data = {'type' : 'error',
                    'error' : True,
                    'error_code' : int(resp['status'])}

        if multi:
            return map(lambda url, data: Url(data, method, url),
                       url_or_urls, data)

        return Url(data, method, url_or_urls)

    def oembed(self, url_or_urls, **kwargs):
        """
        oembed
        """
        return self._get(1, 'oembed', url_or_urls, **kwargs)

    def preview(self, url_or_urls, **kwargs):
        """
        oembed
        """
        return self._get(1, 'preview', url_or_urls, **kwargs)

    def objectify(self, url_or_urls, **kwargs):
        """
        oembed
        """
        return self._get(2, 'objectify', url_or_urls, **kwargs)
