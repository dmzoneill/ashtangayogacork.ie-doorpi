#!/bin/bash
sleep 15
/var/www/html/bin/startvpn.sh
chromium-browser --start-fullscreen http://localhost &
sleep 25
sudo nohup /usr/bin/python3 /var/www/html/shala-manager.py > /tmp/shala &
sudo nohup /usr/bin/python3 /var/www/html/bin/keepalive.py &
(cd /var/www/html/heating; sudo nohup uvicorn --host 0.0.0.0 heater:app)


