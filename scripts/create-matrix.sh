#!/bin/sh

matrix_cmd="{\"site\": ["

for file in ./config/scraper/*.scraper.config; do
    # add \"site\" to job matrix configuration
    site=$(basename $file .scraper.config)
    matrix_cmd="${matrix_cmd} \"${site}\","
done

# strip last comma
matrix_cmd=$(echo ${matrix_cmd} | sed 's/.$//')

matrix_cmd="${matrix_cmd}]}"
echo ${matrix_cmd}