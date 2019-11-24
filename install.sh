#!/bin/bash
# Install this Python package and register to user cron.
# Run in this directory:
# >>> bash install.sh

show_result () {
    echo
    if [ $stat -ne 0 ]; then
        echo $kind failed.
        exit 1
    else
        echo $kind succeeded.
    fi
}

# Install this python package
pip3 install .
stat=$?
kind="pip install"
show_result

# Register to cron
# FIXME: make this configurable and changeable
echo "$(crontab -l ; echo '0 6 * * * briefer send')" | crontab -
stat=$?
kind="Registering to cron"
show_result
