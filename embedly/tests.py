
import unittest

from embedly.client import domain_re
from embedly.models import Url

class EmbedlyTestCase(unittest.TestCase):

    def test_domain_re(self):        
        self.assert_(domain_re.match('pro.embed.ly'))
        self.assert_(domain_re.match('api.embed.ly'))
        self.assert_(domain_re.match('embed.ly') is None)
        self.assert_(domain_re.match('pro.embedly') is None)
        self.assert_(domain_re.match('pro..embed.ly') is None)
        self.assert_(domain_re.match('http://pro.embed.ly') is None)

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

if __name__ == '__main__':
    unittest.main()