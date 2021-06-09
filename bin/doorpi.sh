#!/bin/bash
#rm -rf ~/.mozilla/firefox/*.default/*.sqlite ~/.mozilla/firefox/*default/sessionstore.js
#rm -rf ~/.cache/mozilla/firefox/*.default/*
#rm -rf ~/.cache/midori/
#sleep 15
#sudo nohup /usr/bin/python3 /var/www/html/monitor-clap.py > /tmp/clap &
#sleep 5
#sudo nohup /usr/bin/python3 /var/www/html/heating-manager.py > /tmp/heat &
#sleep 5
sleep 25
sudo nohup /usr/bin/python3 /var/www/html/shala-manager.py > /tmp/shala &
sudo nohup /usr/bin/python3 /var/www/html/bin/keepalive.py &
sleep 10
#midori -e Fullscreen -e Navigationbar -e Statusbar -a http://localhost
chromium-browser --start-fullscreen http://localhost &
#sleep 10
#firefox -url http://127.0.0.1 &
#sleep 25
#xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11
#vncserver -kill :1
#vncserver -geometry 1200x800 -localhost no
#unclutter -idle 0.01 -root

