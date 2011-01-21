from os import environ

from freshen import *

from embedly.client import Embedly

@Given("an embedly endpoint( [^\s]+)?( with key)?$")
def init_api(domain, key_enabled):
  opts = {}

  if domain:
     opts['domain'] = domain

  if key_enabled:
    if not environ.get('EMBEDLY_KEY'):
        raise RuntimeError('Please set env variable $EMBEDLY_KEY')
    opts['key'] = environ["EMBEDLY_KEY"]

  scc.api = Embedly(**opts)

@When("(\w+) is called with the (.*) URLs?( and ([^\s]+) flag)?$")
def call_urls(method, urls, _, flag):
  urls = urls.split(',')
  opts = {}
  if len(urls) == 1:
    opts['url_or_urls'] = urls[0]
  else:
    opts['url_or_urls'] = urls

  if flag:
      opts[flag] = 'true'

  scc.result = getattr(scc.api, method)(**opts)

@Then("(the )?([^\s]+) should be ([^\s]+)")
def check_value(_, key, value):
  if type(scc.result) == list:
    r = []
    for o in scc.result:
      r.append(str(o.get(key)))
    assert_equal(','.join(r), value)

  else:
    assert_equal(str(scc.result.get(key)), value)
