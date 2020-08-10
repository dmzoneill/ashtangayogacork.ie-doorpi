#!/bin/bash 

#/usr/bin/rclone --config /var/lib/motion/rclone.conf move --include *.mkv --include *.jpg /var/lib/motion/ google:/motion/
/usr/bin/rclone --config /var/lib/motion/rclone.conf move --include=*.mkv /var/lib/motion/ google:/motion/
