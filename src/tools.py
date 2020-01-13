# -*- coding: utf-8 -*-

import logging, requests, time, csv, datetime, os

from src import cache, languages

def init_logging(name):
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s]  %(message)s')
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler('scrape.' + name + '.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.DEBUG)

def init_wd():
    today = datetime.date.today().strftime('%Y-%m-%d')
    path = './data/' + today

    if not os.path.exists(path):
        os.makedirs(path)

    return path

@cache.memoize(typed=True, expire=60*60*24*1)
def get_idx_page(url):
    #time.sleep(1)
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

@cache.memoize(typed=True, expire=60*60*24*30)
def get_page(url):
    #time.sleep(1)
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

def is_year(s):
    return len(s) == 4 and s.isdigit()

def make_csv(path):
    f = open(path, 'w')
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow(['Site', 'Link', 'Name', 'Author', 'Publisher', 'Year', 'Language'])
    return w

def save_row(writer, site, link, name, author, publisher, year, language):
    writer.writerow([site, link, name, author, publisher, year, language])

def save_book(writer, site, link, name, author, publisher, year, language):
    books = 0
    records = 0
    if name and language:
        for l in language.split(','):
            save_row(writer, site, link, name, author, publisher, year, l)
            records += 1
        books += 1
    else:
        logging.error('unable to process book page: ' + link)

    return (books, records)

def parse_language(l):
    r = []
    ls = l.lower()

    if ', ' in ls:
        ls = ls.split(', ')
    elif ' / ' in ls:
        ls = ls.split(' / ')
    else:
        ls = [ls]

    for i in ls:
        if i in languages:
            r.append(languages[i])
        else:
            logging.error('unknown language: ' + i)

    return ','.join(r)
