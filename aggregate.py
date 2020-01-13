#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv

def key1(date, site, category):
    return date + ':' + site + ':' + category

def key2(date, site, category, language):
    return date + ':' + site + ':' + category + ':' + language

s1 = dict()
s2 = dict()

for subdir, dirs, files in os.walk('./data'):
    if files:
        date = subdir.split('/')[2]
        for fn in files:
            category = fn.split('.')[0]
            with open(subdir + '/' + fn) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    site = row['Site']
                    language = row['Language']

                    k = key1(date, site, category)
                    if k not in s1:
                        s1[k] = 0
                    s1[k] += 1

                    k = key2(date, site, category, language)
                    if k not in s2:
                        s2[k] = { 'count': 0, 'date': date, 'site': site, 'category': category, 'language': language }
                    s2[k]['count'] += 1

r = sorted(s2.values(), key = lambda x: x['date'] + x['site'] + x['category'] + x['language'], reverse = True)
with open('language-trends.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Date', 'Site', 'Category', 'Language', 'Count', 'Percent'])
    for i in r:
        k = key1(i['date'], i['site'], i['category'])
        writer.writerow([i['date'], i['site'], i['category'], i['language'], i['count'], '%.3f' % (i['count'] * 100.0 / s1[k])])
