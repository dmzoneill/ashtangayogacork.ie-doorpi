#!/bin/bash
sleep 15
/var/www/html/bin/startvpn.sh
sleep 25
sudo nohup /usr/bin/python3 /var/www/html/shala-manager.py > /tmp/shala &
sudo nohup /usr/bin/python3 /var/www/html/bin/keepalive.py &
sudo nohup /usr/bin/python3 /var/www/html/bin/kafkadoor.py &
sleep 10
chromium-browser --start-fullscreen http://localhost &

