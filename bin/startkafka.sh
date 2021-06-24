#!/bin/bash -x

pgrep -af kafka
retval=$?
if [ $retval -eq 1 ]; then
  sudo nohup /usr/bin/python3 /var/www/html/bin/kafkadoor.py
fi
