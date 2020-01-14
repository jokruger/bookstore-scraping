#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, logging, re
from bs4 import BeautifulSoup
from src import tools

site = 'bukva.ua'

tools.init_logging(site)
path = tools.init_wd()

index_pages = 0
book_pages = 0
books = 0
records = 0

# ======

def process_book(writer, url):
    logging.info('\t\t\t' + url)

    global book_pages, books, records
    book_pages += 1

    response = tools.get_page(url)
    page = BeautifulSoup(response.text, 'html.parser')

    name = None
    author = None
    publisher = None
    year = None
    language = None

    card = page.find('div', {'id': 'art_data'})
    if card:
        t = card.find('h1')
        if t:
            name = t.text

        t = card.find('div', {'class': re.compile('.*book-detail.*')})
        if t:
            for i in t.findAll('div'):
                r = i.text.split(':')
                if len(r) == 2:
                    k = r[0].lower().strip().rstrip()
                    v = r[1].strip().rstrip()

                    if k == 'автори':
                        author = v
                    elif k == 'виробник':
                        publisher = v
                    elif k == 'дата видання':
                        year = v
                    elif k == 'мова видання':
                        language = tools.parse_language(v)

    b, r = tools.save_book(writer, site, url, name, author, publisher, year, language)
    books += b
    records += r

def process_idx(writer, url):
    logging.info('\t\t' + url)

    global index_pages
    index_pages += 1

    response = tools.get_idx_page(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.findAll('div', {'class': 'h4'}):
        a = item.find('a')
        if a and '/catalog/browse/' in a['href']:
            process_book(writer, a['href'])

def scrape_new(path):
    logging.info('\tscrape new')

    base = 'https://bukva.ua/ua/catalog/browse/445'

    w = tools.make_csv(path + '/new.csv')
    process_idx(w, base)
    for i in range(29):
        process_idx(w, base + '/%d?' % (i + 2))

def scrape_bestsellers(path):
    logging.info('\tscrape bestsellers')

    w = tools.make_csv(path + '/bestsellers.csv')
    process_idx(w, 'https://bukva.ua/ua/catalog/browse/445?filter%%5Bfilter_type%%5D=notexisit&sort=bestsellers&sort_dir=desc&filter_type=&page=1&g_pp=20')
    for i in range(29):
        process_idx(w, 'https://bukva.ua/ua/catalog/browse/445/%d?filter%%5Bfilter_type%%5D=notexisit&sort=bestsellers&sort_dir=desc&filter_type=&page=1&g_pp=20' % (i + 2))

# ======

logging.info('Processing ' + site)

site_path = path + '/' + site
if not os.path.exists(site_path):
    os.makedirs(site_path)

scrape_new(site_path)
scrape_bestsellers(site_path)

logging.info('\tDone %d index pages, %d book pages, %d books, %d records' % (index_pages, book_pages, books, records))
