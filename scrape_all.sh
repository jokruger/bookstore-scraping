#!/bin/bash

rm -f *.log

./scrape_all_init.py

./scrape_book_ye.py &
./scrape_yakaboo.py &

wait

./aggregate.py

git add --all
