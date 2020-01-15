#!/bin/bash

rm -f *.log

./scrape_all_init.py

./scrape_book_ye.py &
./scrape_yakaboo.py &
./scrape_bukva.py &
./scrape_grenka.py &

wait

./aggregate.py

git add --all
