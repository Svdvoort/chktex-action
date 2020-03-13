#!/bin/bash

config="$1"
args="$2"
root_directory="$3"
recursive="$4"
chktex_output="$5"

chktex_command=(chktex -q)

if [ -n "$config" ]; then
    chktex_command+=(-l $config)
fi

if [ -n "$args" ]; then
    chktex_command+=($args)
fi

if [ -n "$root_directory" ]; then
    cd ${root_directory}
fi

if [ "$recursive" = "True" ]; then
    to_check_files=$(find . -name '*.tex')
else
    to_check_files=$(find . -maxdepth 1 -name '*.tex')
fi

for file in ${to_check_files}
do
    "${chktex_command[@]}" "$file" >> "$chktex_output"
    output_status=$?
    if [ $output_status -ne 0 ]; then
        echo "::warning file=${file}::Unresolved linter warnings"
    fi
done
