#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, logging
from bs4 import BeautifulSoup
from src import tools

site = 'book-ye.com.ua'

tools.init_logging(site)
path = tools.init_wd()

index_pages = 0
book_pages = 0
books = 0
records = 0

# ======

def get_name(page):
    t = page.find('h1', {'class': 'card__title'})
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

    t = page.find('div', {'class': 'card__content card__content--primary'})
    for i in t.findAll('div', {'class': 'card__info'}):
        s = i.text.strip().split(': ')
        if len(s) == 2:
            v = s[1].strip()
            k = s[0].strip().lower()
            if k == 'автор':
                author = v
            elif k == 'видавництво':
                publisher = v
            elif k == 'рік видання':
                year = v
            elif k == 'мова':
                language = tools.parse_language(v)
        else:
            logging.error('unable to parse row ' + str(s))

    b, r = tools.save_book(writer, site, url, name, author, publisher, year, language)
    books += b
    records += r

def process_idx(writer, url, done):
    logging.info('\t\t' + url)

    global index_pages
    index_pages += 1

    response = tools.get_idx_page(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.findAll('a', {'class': 'product__name'}):
        if a['href'] not in done:
            done.add(a['href'])
            process_book(writer, 'https://book-ye.com.ua' + a['href'])
        else:
            logging.error('already done: ' + a['href'])

def scrape_new(path):
    logging.info('\tscrape new')

    base = 'https://book-ye.com.ua/catalog/vydavnytstva/filter/novinka-is-true/'
    done = set()

    w = tools.make_csv(path + '/new.csv')
    process_idx(w, base, done)
    for i in range(29):
        process_idx(w, base + '?PAGEN_1=%d' % (i + 2), done)

def scrape_popular(path):
    logging.info('\tscrape popular')

    base = 'https://book-ye.com.ua/catalog/vydavnytstva/filter/top-is-true/'
    done = set()

    w = tools.make_csv(path + '/popular.csv')
    process_idx(w, base, done)
    process_idx(w, base + '?PAGEN_1=2', done)

# ======

logging.info('Processing ' + site)

site_path = path + '/' + site
if not os.path.exists(site_path):
    os.makedirs(site_path)

scrape_new(site_path)
scrape_popular(site_path)

logging.info('\tDone %d index pages, %d book pages, %d books, %d records' % (index_pages, book_pages, books, records))
