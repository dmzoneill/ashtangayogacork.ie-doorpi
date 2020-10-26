#!/bin/bash
temp=$(cat /var/www/html/scratch/temperature | sed 's/\n//')
hum=$(cat /var/www/html/scratch/humidity | sed 's/\n//')
/usr/bin/curl "https://ashtangayoga.ie/classes/?action=report_temp&temp=$temp&hum=$hum"
