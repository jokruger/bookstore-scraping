#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, logging
from bs4 import BeautifulSoup
from src import tools

site = 'yakaboo.ua'

tools.init_logging(site)
path = tools.init_wd()

index_pages = 0
book_pages = 0
books = 0
records = 0

# ======

def get_name(page):
    t = page.find('div', {'id': 'product-title'})
    if t:
        return t.text.strip()
    return None

def process_book(writer, url):
    logging.info('\t\t\t' + url)

    global book_pages, books, records
    book_pages += 1

    response = tools.get_page(url)
    page = BeautifulSoup(response.text, 'html.parser')

    name = get_name(page)

    author = None
    publisher = None
    year = None
    language = None

    t = page.find('table', {'class': 'product-attributes__table'})
    if t:
        for r in t.findAll('tr'):
            s = r.text.strip().split('\n')
            if len(s) == 2:
                v = s[1].strip()
                k = s[0].strip().lower()
                if k == 'автор':
                    author = v
                elif k == 'видавництво':
                    publisher = v
                elif k == 'мова':
                    language = tools.parse_language(v)
                elif k == 'рік видання':
                    year = v
            else:
                logging.error('unable to parse row ' + str(s))

    b, r = tools.save_book(writer, site, url, name, author, publisher, year, language)
    books += b
    records += r

def process_idx(writer, url):
    logging.info('\t\t' + url)

    global index_pages
    index_pages += 1

    response = tools.get_idx_page(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.findAll('li', {'class': 'item'}):
        a = item.find('a')
        if a:
            process_book(writer, a['href'])

def scrape_new(path):
    logging.info('\tscrape new')

    w = tools.make_csv(path + '/new.csv')
    process_idx(w, 'https://www.yakaboo.ua/ua/top100/category/newarrival/id/4723/')
    for i in range(29):
        process_idx(w, 'https://www.yakaboo.ua/ua/top100/category/newarrival/id/4723/?p=%d' % (i + 2))

def scrape_popular(path):
    logging.info('\tscrape popular')

    w = tools.make_csv(path + '/popular.csv')
    process_idx(w, 'https://www.yakaboo.ua/ua/top100/category/popular/id/4723/')
    for i in range(29):
        process_idx(w, 'https://www.yakaboo.ua/ua/top100/category/popular/id/4723/?p=%d' % (i + 2))

# ======

logging.info('Processing ' + site)

site_path = path + '/' + site
if not os.path.exists(site_path):
    os.makedirs(site_path)

scrape_new(site_path)
scrape_popular(site_path)

logging.info('\tDone %d index pages, %d book pages, %d books, %d records' % (index_pages, book_pages, books, records))
