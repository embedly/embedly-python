from __future__ import unicode_literals
import re
import json

try:  # pragma: no cover
    import unittest2 as unittest  # Python 2.6   # pragma: no cover
except ImportError:  # pragma: no cover
    import unittest  # pragma: no cover

from embedly.client import Embedly
from embedly.models import Url


class UrlTestCase(unittest.TestCase):
    def test_model(self):
        data = {
            'provider_url': 'http://www.google.com/',
            'safe': True,
            'description': 'Google',
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
        obj = Url(data, 'preview', 'http://original.url.com/')

        self.assertEqual(len(obj), 16)
        self.assertEqual(len(obj.values()), 16)
        self.assertEqual(len(obj.keys()), 16)
        self.assertEqual(len(obj.items()), 16)

        # check for expected data
        self.assertTrue('type' in obj.keys())
        self.assertTrue('html' in obj.values())
        self.assertEqual(obj['type'], 'html')
        self.assertEqual(obj.get('type'), 'html')
        self.assertEqual(obj.data['type'], 'html')
        self.assertEqual(obj.data.get('type'), 'html')

        # our special attrs shouldn't be in the data dict
        self.assertFalse('method' in obj.keys())
        with self.assertRaises(KeyError):
            obj['method']

        # attrs and data dict values should be separate
        self.assertEqual(obj.original_url, 'http://original.url.com/')

        obj.new_attr = 'attr value'
        obj['new_key'] = 'dict value'
        self.assertEqual(obj.new_attr, 'attr value')
        self.assertEqual(obj['new_key'], 'dict value')

    def test_model_data_can_serialize(self):
        obj = Url({'hash': {'key': 'value'},
                   'none': None,
                   'empty': '',
                   'float': 1.234,
                   'int': 1,
                   'string': 'string',
                   'array': [0, -1]})
        unserialzed = json.loads(json.dumps(obj.data))
        self.assertDictEqual(obj.data, unserialzed)


class EmbedlyTestCase(unittest.TestCase):
    def setUp(self):
        self.key = 'internal'

    def test_requires_api_key(self):
        with self.assertRaises(ValueError):
            Embedly()._get(1, "test", "http://fake")

    def test_requires_url(self):
        with self.assertRaises(ValueError):
            Embedly(self.key)._get(1, "test", None)

    def test_exception_on_too_many_urls(self):
        urls = ['http://embed.ly'] * 21
        with self.assertRaises(ValueError):
            Embedly(self.key)._get(1, "test", urls)

    def test_provider(self):
        http = Embedly(self.key)

        obj = http.oembed('http://www.scribd.com/doc/13994900/Easter')

        self.assertEqual(obj['provider_url'], 'http://www.scribd.com/')

        obj = http.oembed('http://www.scribd.com/doc/28452730/Easter-Cards')
        self.assertEqual(obj['provider_url'], 'http://www.scribd.com/')

        obj = http.oembed('http://www.youtube.com/watch?v=Zk7dDekYej0')
        self.assertEqual(obj['provider_url'], 'http://www.youtube.com/')

        obj = http.oembed('http://yfrog.com/h22eu4j')
        self.assertEqual(obj['provider_url'], 'http://yfrog.com')

    def test_providers(self):
        http = Embedly(self.key)

        objs = list(http.oembed(['http://www.scribd.com/doc/13994900/Easter',
                                 'http://www.scribd.com/doc/28452730/Easter-Cards']))

        self.assertEqual(objs[0]['provider_url'], 'http://www.scribd.com/')
        self.assertEqual(objs[1]['provider_url'], 'http://www.scribd.com/')

        objs = list(http.oembed(['http://www.youtube.com/watch?v=Zk7dDekYej0',
                                 'http://yfrog.com/h22eu4']))
        self.assertEqual(objs[0]['provider_url'], 'http://www.youtube.com/')
        self.assertEqual(objs[1]['provider_url'], 'http://yfrog.com')

    def test_error(self):
        http = Embedly(self.key)

        obj = http.oembed('http://www.embedly.com/this/is/a/bad/url')
        self.assertTrue(obj['error'])
        obj = http.oembed('http://blog.embed.ly/lsbsdlfldsf/asdfkljlas/klajsdlfkasdf')
        self.assertTrue(obj['error'])
        obj = http.oembed('http://twitpic/nothing/to/see/here')
        self.assertTrue(obj['error'])

    def test_multi_errors(self):
        http = Embedly(self.key)

        objs = list(http.oembed(['http://www.embedly.com/this/is/a/bad/url',
                                 'http://blog.embed.ly/alsd/slsdlf/asdlfj']))

        self.assertEqual(objs[0]['type'], 'error')
        self.assertEqual(objs[1]['type'], 'error')

        objs = list(http.oembed(['http://blog.embed.ly/lsbsdlfldsf/asdf/kl',
                                 'http://twitpic.com/nothing/to/see/here']))
        self.assertEqual(objs[0]['type'], 'error')
        self.assertEqual(objs[1]['type'], 'error')

        objs = list(http.oembed(['http://blog.embed.ly/lsbsdlfldsf/asdf/kl',
                                 'http://yfrog.com/h22eu4j']))
        self.assertEqual(objs[0]['type'], 'error')
        self.assertEqual(objs[1]['type'], 'photo')

        objs = list(http.oembed(['http://yfrog.com/h22eu4j',
                                 'http://www.scribd.com/asdf/asdf/asdfasdf']))
        self.assertEqual(objs[0]['type'], 'photo')
        self.assertEqual(objs[1]['type'], 'error')

    def test_raw_content_in_request(self):
        client = Embedly(self.key)
        response = client.oembed(
            'http://www.scribd.com/doc/13994900/Easter',
            raw=True)

        self.assertEqual(response['raw'], response.data['raw'])

        parsed = json.loads(response['raw'].decode('utf-8'))
        self.assertEqual(response['type'], parsed['type'])

    def test_regex_url_matches(self):
        regex = [
            'http://.*youtube\\.com/watch.*',
            'http://www\\.vimeo\\.com/.*']
        client = Embedly(self.key)
        client._regex = re.compile('|'.join(regex))

        self.assertTrue(
            client.is_supported('http://www.youtube.com/watch?v=Zk7dDekYej0'))
        self.assertTrue(
            client.is_supported('http://www.vimeo.com/18150336'))
        self.assertFalse(
            client.is_supported('http://vimeo.com/18150336'))
        self.assertFalse(
            client.is_supported('http://yfrog.com/h22eu4j'))

    def test_services_can_be_manually_configured(self):
        client = Embedly(self.key)
        client.services = ['nothing', 'like', 'real', 'response', 'data']

        self.assertTrue('nothing' in client.get_services())
        self.assertEqual(len(client.get_services()), 5)

    def test_get_services_retrieves_data_and_builds_regex(self):
        client = Embedly(self.key)
        client.get_services()

        self.assertGreater(len(client.services), 0)
        self.assertTrue(client.regex.match('http://yfrog.com/h22eu4j'))

    def test_extract(self):
        client = Embedly(self.key)
        response = client.extract('http://vimeo.com/18150336')

        self.assertEqual(response.method, 'extract')
        self.assertEqual(response['provider_name'], 'Vimeo')

    def test_preview(self):
        client = Embedly(self.key)
        response = client.preview('http://vimeo.com/18150336')

        self.assertEqual(response.method, 'preview')
        self.assertEqual(response['provider_name'], 'Vimeo')

    def test_objectify(self):
        client = Embedly(self.key)
        response = client.objectify('http://vimeo.com/18150336')

        self.assertEqual(response.method, 'objectify')
        self.assertEqual(response['provider_name'], 'Vimeo')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()  # pragma: no cover
