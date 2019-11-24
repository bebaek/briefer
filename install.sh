#!/bin/bash
# Install this Python package and register to user cron.
# Run in this directory:
# >>> bash install.sh

# pip puts the bin file here
bin_path="$HOME/.local/bin"

show_result () {
    echo
    if [ $stat -ne 0 ]; then
        echo $kind failed.
        exit 1
    else
        echo $kind succeeded.
    fi
}

# (Re-)Install this python package
pip3 install --force-reinstall .
stat=$?
kind="pip install"
show_result

# Configure app
"$bin_path/briefer" config
stat=$?
kind="Config"
show_result

# Register to user cron
# FIXME: make this configurable and changeable
echo "$(crontab -l ; echo 0 6 '* * *' $bin_path/briefer send)" | crontab -
stat=$?
kind="Registering to cron"
show_result
