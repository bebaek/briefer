#!/bin/bash
# Start local smtpd
echo Start: smtpd
python -m smtpd -c DebuggingServer -n localhost:1025
