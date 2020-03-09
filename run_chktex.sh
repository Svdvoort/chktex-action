#!/bin/sh

set -e

config="$1"
args="$2"
warnings_as_errors="$3"

python3 /root/run_action.py $config $args $warnings_as_errors
#python3 /tmp/action/run_action.py $config $args
