
import os
import unittest

from embedly.client import Embedly
from embedly.models import Url

class EmbedlyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.key = 'internal' # os.environ['EMBEDLY_API_KEY']

        if not self.key:
            raise ValueError('Set envirnomental varible EMBEDLY_API_KEY '+\
                             'before running these tests like so: $ export '+\
                             'EMBEDLY_API_KEY=key')

        super(EmbedlyTestCase, self).__init__(*args, **kwargs)

    def test_model(self):
        data = {
            u'provider_url': u'http://www.google.com/',
            u'safe': True,
            u'description': u'Google',
            u'original_url': u'http://google.com/',
            u'url': u'http://www.google.com/',
            u'type': u'html',
            u'object': {},
            u'provider_display': u'www.google.com',
            u'author_name': None,
            u'favicon_url': u'http://www.google.com/favicon.ico',
            u'place': {},
            u'author_url': None,
            u'images': [
                {u'url': u'http://www.google.com/intl/en_ALL/images/srpr/logo1w.png',
                 u'width': 275,
                 u'height': 95}],
            u'title': u'Google',
            u'provider_name': u'Google',
            u'cache_age': 86400,
            u'embeds': []
        }

        obj = Url(data, 'preview', 'http://google.com/')

        self.assert_(len(obj) is 17)
        self.assert_(len(obj.values()) is 17)
        self.assert_(len(obj.keys()) is 17)
        self.assert_(len(obj.items()) is 17)

        self.assert_('type' in obj.keys())
        self.assert_('html' in obj.values())

        #Get the object
        self.assert_(obj.type == 'html')
        self.assert_(obj['type'] == 'html')
        self.assert_(obj.get('type') == 'html')

        #nope
        self.assert_(obj.nothing is None)

        obj.nothing = 'something'
        self.assert_(obj.nothing == 'something')

        obj['nothing'] = 'maybe'
        self.assert_(obj['nothing'] == 'maybe')

        del obj['nothing']
        self.assert_(obj.nothing is None)

        #Deep Get attrs
        self.assert_(obj.images[0].width is 275)
        self.assert_(obj.images[0].nothing is None)
        self.assert_(obj.object.type is None)

    def test_provider(self):
        http = Embedly(self.key)

        obj = http.oembed('http://www.scribd.com/doc/13994900/Easter')
        self.assert_(obj.provider_url == 'http://www.scribd.com/')

        obj = http.oembed('http://www.scribd.com/doc/28452730/Easter-Cards')
        self.assert_(obj.provider_url == 'http://www.scribd.com/')

        obj = http.oembed('http://www.youtube.com/watch?v=Zk7dDekYej0')
        self.assert_(obj.provider_url == 'http://www.youtube.com/')

        obj = http.oembed('http://yfrog.com/h22eu4j')
        self.assert_(obj.provider_url == 'http://yfrog.com')

    def test_providers(self):
        http = Embedly(self.key)

        objs = http.oembed(['http://www.scribd.com/doc/13994900/Easter',
                            'http://www.scribd.com/doc/28452730/Easter-Cards'])
        self.assert_(objs[0].provider_url == 'http://www.scribd.com/')
        self.assert_(objs[1].provider_url == 'http://www.scribd.com/')

        objs = http.oembed(['http://www.youtube.com/watch?v=Zk7dDekYej0',
                            'http://yfrog.com/h22eu4'])
        self.assert_(objs[0].provider_url == 'http://www.youtube.com/')
        self.assert_(objs[1].provider_url == 'http://yfrog.com')

    def test_error(self):
        http = Embedly(self.key)

        obj = http.oembed('http://www.embedly.com/this/is/a/bad/url')
        self.assert_(obj.error is True, obj.dict)
        obj = http.oembed('http://blog.embed.ly/lsbsdlfldsf/asdfkljlas/klajsdlfkasdf')
        self.assert_(obj.error is True, obj.dict)
        obj = http.oembed('http://twitpic/nothing/to/see/here')
        self.assert_(obj.error is True, obj.dict)

    def test_multi_errors(self):
        http = Embedly(self.key)

        objs = http.oembed(['http://www.embedly.com/this/is/a/bad/url',
                            'http://blog.embed.ly/alsd/slsdlf/asdlfj'])
        self.assert_(objs[0].type == 'error', objs[0].dict)
        self.assert_(objs[1].type == 'error', objs[1].dict)

        objs = http.oembed(['http://blog.embed.ly/lsbsdlfldsf/asdf/kl',
                            'http://twitpic.com/nothing/to/see/here'])
        self.assert_(objs[0].type == 'error',objs[0].dict)
        self.assert_(objs[1].type == 'error',objs[1].dict)

        objs = http.oembed(['http://blog.embed.ly/lsbsdlfldsf/asdf/kl',
                            'http://yfrog.com/h22eu4j'])
        self.assert_(objs[0].type == 'error',objs[0].dict)
        self.assert_(objs[1].type == 'photo',objs[1].dict)

        objs = http.oembed(['http://yfrog.com/h22eu4j',
                            'http://www.scribd.com/asdf/asdf/asdfasdf'])
        self.assert_(objs[0].type == 'photo',objs[0].dict)
        self.assert_(objs[1].type == 'error',objs[1].dict)


    def test_too_many_urls(self):
        http = Embedly(self.key)

        urls = ['http://embed.ly'] * 21
        try:
            http.oembed(urls)
            self.fail('too many urls, should have thrown an error')
        except Exception, e:
            self.assertTrue(type(e), ValueError)

if __name__ == '__main__':
    unittest.main()