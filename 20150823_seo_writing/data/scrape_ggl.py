# coding=utf-8
"""
Uses Selenium with Firefox to scrape search results from Google search.

* Assumes that the user is NOT logged into Google.
* Requires queries.txt to be present in the working directory.
  queries.txt should contain space-separated search terms, one in each line ie
    ...
    渋谷 ラーメン
    家具 一人暮らし おすすめ　
    ...

Search result is saved to disk using cPickle.
"""
from selenium import webdriver
from parse_result import parse, parse_navigation
from models import SearchResult
import time, random, cPickle

WAIT = 4  # Number of seconds between successive GET requests
BASE_URL = 'https://www.google.co.jp'


def get_text_with_query(driver, query):
    return get_text(driver, BASE_URL + "/search?ie=UTF-8&q=%s" % query)


def get_text(driver, url):
    driver.get(url)
    return driver.page_source


def save_search_results(sr):
    with open('results.pickle', 'wb') as f:
        p = cPickle.Pickler(f)
        p.dump(sr)


if __name__ == '__main__':
    with open('queries.txt', 'r') as f:
        queries = f.readlines()
    random.shuffle(queries)
    search_results = []
    driver = webdriver.Firefox()
    for query in queries:
        if not query:
            continue
        src = get_text_with_query(driver, query)
        sr = SearchResult()
        sr.results += parse(src)
        sr.query = query

        time.sleep(WAIT)

        more_pages = parse_navigation(src)
        for p in more_pages:
            path = p.get('url')
            t = get_text(driver, BASE_URL+path)
            time.sleep(WAIT)
            buff = parse(t)
            sr.results += buff
        search_results.append(sr)

    driver.close()
    save_search_results(search_results)
