#!/bin/sh
export GOTHAM_PAGE_DIR_LOCAL=/home/scott/Programs/gotham-city-music-collective-website/public_html
export GOTHAM_PAGE_DIR_SERVER=/home/u652333289/domains/gothamcitymusic.org/public_html
rsync -a --verbose --update --progress -t -r $GOTHAM_PAGE_DIR_LOCAL $GOTHAM_PAGE_DIR_SERVER
