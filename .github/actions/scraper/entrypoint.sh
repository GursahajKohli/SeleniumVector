#!/bin/sh -l

##########################
# arguments: $1 = company
##########################

# setup environment
pip install -r src/requirements.txt

# start docker-splash
sh scripts/run-splash.sh &

# run scraper script and store output
cd src/scraper
python3 scraper ../../config/${1}.scraper.config ../../${1}.xml