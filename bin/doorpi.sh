#!/bin/bash
rm -rf ~/.mozilla/firefox/*.default/*.sqlite ~/.mozilla/firefox/*default/sessionstore.js
rm -rf ~/.cache/mozilla/firefox/*.default/*
rm -rf ~/.cache/midori/

nohup /usr/bin/python3 /var/www/html/monitor-clap.py > /tmp/clap &
nohup /usr/bin/python /var/www/html/heating-manager.py > /tmp/heat &
#midori -e Fullscreen -e Navigationbar -e Statusbar -a http://localhost
sleep 10
firefox -url http://127.0.0.1 &
sleep 25
xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11
#vncserver -kill :1
#vncserver -geometry 1200x800 -localhost no
#unclutter -idle 0.01 -root

