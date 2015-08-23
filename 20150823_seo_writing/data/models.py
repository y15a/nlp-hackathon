import requests


class Page(object):

    def __init__(self, url='', src='', title=''):
        self.url = url
        self.src = src
        self.title = title
        self.body = ''

    def __str__(self):
        return self.url + '\n' + self.src

    def to_dict(self):
        obj = {}
        obj['url'] = self.url
        obj['src'] = self.src
        obj['title'] = self.title
        obj['body'] = self.body
        return obj


class SearchResult(object):

    def __init__(self, *args, **kwargs):
        self.query = ''
        self.results = []

    def __unicode__(self):
        return u'\n'.join([r.title + ' - ' + r.url for r in self.results])

    def __str__(self):
        return unicode(self).encode('utf8')

    def to_dict(self):
        obj = {}
        obj['query'] = self.query
        obj['results'] = []
        for r in self.results:
            obj['results'].append(r.to_dict())
        return obj

