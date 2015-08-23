import requests


class Page(object):

    def __init__(self, url='', src='', title=''):
        self.url = url
        self.src = src
        self.title = title
        self.body = ''

    def __str__(self):
        return self.url + '\n' + self.src


class SearchResult(object):

    def __init__(self, *args, **kwargs):
        self.query = ''
        self.results = []

    def __unicode__(self):
        return u'\n'.join([r.title + ' - ' + r.url for r in self.results])

    def __str__(self):
        return unicode(self).encode('utf8')
