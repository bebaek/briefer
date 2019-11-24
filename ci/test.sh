#!/bin/bash
# Run tests

show_result () {
    echo
    if [ $stat -ne 0 ]; then
        echo $kind failed.
        exit 1
    else
        echo $kind succeeded.
    fi
}

# Launch test
briefer -h
stat=$?
kind="Launch test"
show_result

# Unit tests
python -m unittest
stat=$?
kind="Unit tests"
show_result
