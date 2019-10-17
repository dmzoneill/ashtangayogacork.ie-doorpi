#!/bin/bash

/usr/bin/curl "https://ashtangayoga.ie/classes/?action=download_schedule" -o /var/www/html/scratch/schedule.json
chmod 777 /var/www/html/scratch/schedule.json
