#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, logging
from bs4 import BeautifulSoup
from src import tools

site = 'grenka.ua'

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

    card = page.find('div', {'class': 'xsp'})
    if card:
        t = card.find('h1')
        if t:
            name = t.text.strip()

        for i in card.findAll('li'):
            t = i.text.strip().rstrip().split('\n')
            if len(t) == 3:
                k = t[0].strip().lower()
                v = t[2].strip()

                if k == 'автор(ы)':
                    author = v
                elif k == 'издательство':
                    publisher = v
                elif k == 'год издания':
                    year = v
                elif k == 'язык издания':
                    language = tools.parse_language(v)

    b, r = tools.save_book(writer, site, url, name, author, publisher, year, language)
    books += b
    records += r

def process_idx(writer, url, done):
    logging.info('\t\t' + url)

    global index_pages
    index_pages += 1

    response = tools.get_idx_page(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    t = soup.find('div', {'id': 'xsrch-items'})
    if t:
        for a in t.findAll('a', {'class': 'y20'}):
            if a['href'] not in done:
                done.add(a['href'])
                process_book(writer, a['href'])
            else:
                logging.error('already done: ' + a['href'])

def scrape_new(path):
    logging.info('\tscrape new')

    base = 'https://grenka.ua/books/new'
    done = set()

    w = tools.make_csv(path + '/new.csv')
    process_idx(w, base, done)
    for i in range(29):
        process_idx(w, base + '?p=%d' % (i + 2), done)

def scrape_bestsellers(path):
    logging.info('\tscrape bestsellers')

    base = 'https://grenka.ua/books/best'
    done = set()

    w = tools.make_csv(path + '/bestsellers.csv')
    process_idx(w, base, done)
    for i in range(20):
        process_idx(w, base + '?p=%d' % (i + 2), done)

# ======

logging.info('Processing ' + site)

site_path = path + '/' + site
if not os.path.exists(site_path):
    os.makedirs(site_path)

scrape_new(site_path)
scrape_bestsellers(site_path)

logging.info('\tDone %d index pages, %d book pages, %d books, %d records' % (index_pages, book_pages, books, records))
