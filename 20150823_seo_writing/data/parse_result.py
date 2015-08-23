from bs4 import BeautifulSoup as bs
from models import Page


def parse(s):
    '''Takes source HTML and returns list of Pages
    '''
    results = []
    soup = bs(s)
    for result in soup.find_all(class_='g'):
        title = url = ''
        try:
            title = result.find('h3').find('a').text
            url = result.find('h3').find('a')['href']
        except AttributeError:
            pass
        if title and url:
            page = Page(title=title, url=url)
            results.append(page)
    return results


def parse_navigation(s):
    '''Takes source HTML and returns list of URLs
    '''
    soup = bs(s)
    nav = soup.find(id='navcnt')
    pages = []
    if nav:
        for a in nav.find_all('a', class_='fl'):
            index = a.txt
            url = a['href']
            pages.append(dict(index=index, url=url))
    return pages


if __name__ == '__main__':
    import sys
    s = sys.stdin.read()
    print(''.join(parse(s)))
