from __future__ import unicode_literals
import unittest

from embedly.client import Embedly
from embedly.models import Url

class EmbedlyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.key = 'internal'

        if not self.key:
            raise ValueError('Set envirnomental varible EMBEDLY_API_KEY ' +
                             'before running these tests like so: $ export ' +
                             'EMBEDLY_API_KEY=key')

        super(EmbedlyTestCase, self).__init__(*args, **kwargs)

    def test_model(self):
        data = {
            'provider_url': 'http://www.google.com/',
            'safe': True,
            'description': 'Google',
            'original_url': 'http://google.com/',
            'url': 'http://www.google.com/',
            'type': 'html',
            'object': {},
            'provider_display': 'www.google.com',
            'author_name': None,
            'favicon_url': 'http://www.google.com/favicon.ico',
            'place': {},
            'author_url': None,
            'images': [
                {'url': 'http://www.google.com/intl/en_ALL/images/srpr/logo1w.png',
                 'width': 275,
                 'height': 95}],
            'title': 'Google',
            'provider_name': 'Google',
            'cache_age': 86400,
            'embeds': []
        }

        obj = Url(data, 'preview', 'http://google.com/')

        self.assertTrue(len(obj) is 17)
        self.assertTrue(len(obj.values()) is 17)
        self.assertTrue(len(obj.keys()) is 17)
        self.assertTrue(len(obj.items()) is 17)

        self.assertTrue('type' in obj.keys())
        self.assertTrue('html' in obj.values())

        #Get the object
        self.assertTrue(obj.type == 'html')
        self.assertTrue(obj['type'] == 'html')
        self.assertTrue(obj.get('type') == 'html')

        #nope
        self.assertTrue(obj.nothing is None)

        obj.nothing = 'something'
        self.assertTrue(obj.nothing == 'something')

        obj['nothing'] = 'maybe'
        self.assertTrue(obj['nothing'] == 'maybe')

        del obj['nothing']
        self.assertTrue(obj.nothing is None)

        #Deep Get attrs
        self.assertTrue(obj.images[0].width is 275)
        self.assertTrue(obj.images[0].nothing is None)
        self.assertTrue(obj.object.type is None)

    def test_provider(self):
        http = Embedly(self.key)

        obj = http.oembed('http://www.scribd.com/doc/13994900/Easter')
        self.assertTrue(obj.provider_url == 'http://www.scribd.com/')

        obj = http.oembed('http://www.scribd.com/doc/28452730/Easter-Cards')
        self.assertTrue(obj.provider_url == 'http://www.scribd.com/')

        obj = http.oembed('http://www.youtube.com/watch?v=Zk7dDekYej0')
        self.assertTrue(obj.provider_url == 'http://www.youtube.com/')

        obj = http.oembed('http://yfrog.com/h22eu4j')
        self.assertTrue(obj.provider_url == 'http://yfrog.com')

    def test_providers(self):
        http = Embedly(self.key)

        objs = list(http.oembed(['http://www.scribd.com/doc/13994900/Easter',
                                 'http://www.scribd.com/doc/28452730/Easter-Cards']))
        self.assertTrue(objs[0].provider_url == 'http://www.scribd.com/')
        self.assertTrue(objs[1].provider_url == 'http://www.scribd.com/')

        objs = list(http.oembed(['http://www.youtube.com/watch?v=Zk7dDekYej0',
                                 'http://yfrog.com/h22eu4']))
        self.assertTrue(objs[0].provider_url == 'http://www.youtube.com/')
        self.assertTrue(objs[1].provider_url == 'http://yfrog.com')

    def test_error(self):
        http = Embedly(self.key)

        obj = http.oembed('http://www.embedly.com/this/is/a/bad/url')
        self.assertTrue(obj.error is True, obj.dict)
        obj = http.oembed('http://blog.embed.ly/lsbsdlfldsf/asdfkljlas/klajsdlfkasdf')
        self.assertTrue(obj.error is True, obj.dict)
        obj = http.oembed('http://twitpic/nothing/to/see/here')
        self.assertTrue(obj.error is True, obj.dict)

    def test_multi_errors(self):
        http = Embedly(self.key)

        objs = list(http.oembed(['http://www.embedly.com/this/is/a/bad/url',
                                 'http://blog.embed.ly/alsd/slsdlf/asdlfj']))
        self.assertTrue(objs[0].type == 'error', objs[0].dict)
        self.assertTrue(objs[1].type == 'error', objs[1].dict)

        objs = list(http.oembed(['http://blog.embed.ly/lsbsdlfldsf/asdf/kl',
                                 'http://twitpic.com/nothing/to/see/here']))
        self.assertTrue(objs[0].type == 'error',objs[0].dict)
        self.assertTrue(objs[1].type == 'error',objs[1].dict)

        objs = list(http.oembed(['http://blog.embed.ly/lsbsdlfldsf/asdf/kl',
                            'http://yfrog.com/h22eu4j']))
        self.assertTrue(objs[0].type == 'error',objs[0].dict)
        self.assertTrue(objs[1].type == 'photo',objs[1].dict)

        objs = list(http.oembed(['http://yfrog.com/h22eu4j',
                            'http://www.scribd.com/asdf/asdf/asdfasdf']))
        self.assertTrue(objs[0].type == 'photo',objs[0].dict)
        self.assertTrue(objs[1].type == 'error',objs[1].dict)


    def test_too_many_urls(self):
        http = Embedly(self.key)

        urls = ['http://embed.ly'] * 21
        try:
            http.oembed(urls)
            self.fail('too many urls, should have thrown an error')
        except Exception as e:
            self.assertTrue(type(e), ValueError)

if __name__ == '__main__':
    unittest.main()