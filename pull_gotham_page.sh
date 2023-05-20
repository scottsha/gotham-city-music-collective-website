#!/bin/sh
. ./page_syncing_variables.sh
rsync -a --verbose --update --progress -t -r $GOTHAM_PAGE_DIR_SERVER/public_html $GOTHAM_PAGE_DIR_LOCAL
