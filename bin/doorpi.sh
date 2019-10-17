#!/bin/bash
rm -rf ~/.mozilla/firefox/*.default/*.sqlite ~/.mozilla/firefox/*default/sessionstore.js
rm -rf ~/.cache/mozilla/firefox/*.default/*
rm -rf ~/.cache/midori/

nohup /usr/bin/python3 /var/www/html/monitor-clap.py > /tmp/clap &
nohup /usr/bin/python /var/www/html/heating-manager.py > /tmp/heat &
midori -e Fullscreen -a http://localhost
sleep 15
#xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11
#vncserver -kill :1
#vncserver -geometry 1200x800 -localhost no
unclutter -idle 0.01 -root

