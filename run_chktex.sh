#!/bin/sh

set -e

config="$1"
args="$2"

python3 run_action.py $config $args
#python3 /tmp/action/run_action.py $config $args
