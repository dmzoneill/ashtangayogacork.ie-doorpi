#!/usr/bin/python3
import os
from pathlib import Path
import subprocess
import signal
import time

def main():
    plugs = ["192.168.8.3", "192.168.8.4", "192.168.8.5", "192.168.8.6"]

    while True:
        time.sleep(1)
        try:
            for address in plugs:
                res = subprocess.call(['ping', '-c', '3', address])
                if res == 0:
                    print("ping to " + address + "OK")
                elif res == 2:
                    print("no response from" + address)
                else:
                    print("ping to " + address + " failed!")
        except:
            print("dont care")

if __name__== "__main__":
   main()
