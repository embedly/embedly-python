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
    def __init__(self, user_agent=USER_AGENT, domain=None, key=None):
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
        if not domain:
            if key:
                domain = 'pro.embed.ly'
            else:
                domain = 'api.embed.ly'

        if not domain_re.match(domain):
            raise ValueError(
                'Invalid Domain: %s. api.embed.ly or pro.embed.ly' % domain)

        if domain == 'pro.embed.ly' and key is None:
            raise ValueError('domain: pro.embed.ly requires a key.')

        self.user_agent = user_agent
        self.domain = domain
        self.key = key
        self.services = []

    def get_services(self):
        """
        get_services makes call to services end point of api.embed.ly to fetch the
        list of supported providers and their regexes
        """

        if self.services: return self.services

        url = 'http://' + self.domain +'/1/services/python'

        http = httplib2.Http()
        headers = {'User-Agent' : self.user_agent}
        resp, content = http.request(url, headers=headers)

        if resp['status'] == '200':
            resp_data = json.loads(content)
            self.services = resp_data

        return self.services

    def _get(self, version, method, url_or_urls, **kwargs):
        """
        _get makes the actual call to pro.embed.ly/api.embed.ly
        """

        query = ''

        if self.key:

            _regex = []
            for each in self.get_services():
                _regex.append('|'.join(each.get('regex',[])))

            service_regex = re.compile('|'.join(_regex))

            return_list = []
            if isinstance(url_or_urls, list):
                new_url_or_urls = []
                for each in url_or_urls:
                    if service_regex.match(each):
                        return_list.append('valid')
                        new_url_or_urls.append(each)
                    else:
                        return_list.append({
                            'type' : 'error',
                            'error' : True,
                            'error_code' : 404,
                            'error_message': 'This service requires an Embedly Pro account',
                            'url': each,
                            'version': '1.0'
                        })
                old_url_or_urls = url_or_urls
                url_or_urls = new_url_or_urls
            else:
                if not service_regex.match(url_or_urls):
                    data =  {
                            'type' : 'error',
                            'error' : True,
                            'error_code' : 404,
                            'error_message': 'This service requires an Embedly Pro account',
                            'url': url_or_urls,
                            'version': '1.0'
                    }
                    return Url(data, method, url_or_urls)
                else:
                    return_list = 'valid'

        data = {}
        if url_or_urls:

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

            if resp['status'] == '200':
                data = json.loads(content)
            else:
                data = {'type' : 'error',
                        'error' : True,
                        'error_code' : int(resp['status'])}


        if self.key:
            if isinstance(return_list, list):
                if 'valid' in return_list:
                    _data = []
                    if isinstance(data, list):
                        data.reverse()
                        for each in return_list:
                            if each == 'valid':
                                _data.append(data.pop())
                            else:
                                _data.append(each)
                    elif isinstance(data, dict) and data.get('type','') == 'error':
                        for each in return_list:
                            if each == 'valid':
                                _data.append(data)
                            else:
                                _data.append(each)
                else:
                    _data = return_list

                data = _data
                url_or_urls = old_url_or_urls

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
