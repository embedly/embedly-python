"""
Client
======

The embedly object that interacts with the service
"""
import re
import urllib
import httplib2
import json

from models import Url

domain_re = re.compile('^(api|pro)\.embed\.ly$')
USER_AGENT = 'Mozilla/5.0 (compatible; embedly-python/0.2;)'

class Embedly(object):
    """
    Client
    
    """
    def __init__(self, user_agent=USER_AGENT, domain='api.embed.ly', key=None):
        """
        Initialize the Embedly client 
        
        :param user_agent: User Agent passed to Embedly
        :type user_agent: str
        :param domain: Domain you want the client to use '(api|pro).embed.ly'
        :type domain: str
        :param key: Embedly Pro key
        :type key: str

        :returns: None
        :raises: ValueError
        """
        if not domain_re.match(domain):
            raise ValueError(
                'Invalid Domain: %s. api.embed.ly or pro.embed.ly' % domain)
        
        if domain == 'pro.embed.ly' and key is None:
            raise ValueError('domain: pro.embed.ly requires a key.')
        
        self.user_agent = user_agent
        self.domain = domain
        self.key = key

    def _get(self, version, method, url_or_urls, **kwargs):
        """
        _get makes the actual call to pro.embed.ly
        """
        query = ''
        if isinstance(url_or_urls, list):
            query = 'urls=%s&' % ','.join([urllib.quote(url) for url in url_or_urls])
        else:
            kwargs['url'] = url_or_urls

        if self.key and self.domain == 'pro.embed.ly':
            kwargs['key'] = self.key

        query += urllib.urlencode(kwargs)

        url = 'http://%s/%s/%s?%s' % (self.domain, version, method, query)

        http = httplib2.Http()

        headers = {'User-Agent' : self.user_agent}

        resp, content = http.request(url, headers=headers)

        data = {}
        if resp['status'] == '200':
            data = json.loads(content)
        else:
            data = {'error' : True,
                    'error_code' : int(resp['status'])}

        print data

        if isinstance(url_or_urls, list):
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