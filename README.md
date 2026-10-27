# Ashtanga Yoga Cork DoorPi

<p align="center">
  <img src=".github/logo.png" alt="ashtangayogacork.ie-doorpi logo" width="128" />
</p>

A Raspberry Pi controller for the Ashtanga Yoga Cork studio. It opens the
studio door and runs the heating around the class schedule.

## What it does

- `shala-manager.py` reads the class schedule from
  `scratch/schedule.json` and switches the heaters on and off around
  today's classes, using readings from a DHT temperature and humidity
  sensor.
- `heating` controls TP-Link Kasa and Tapo P100 smart plugs, and
  `heating/heater.py` exposes the heaters through a FastAPI app served
  with uvicorn.
- `door/index.php` opens the door through a GPIO relay when called with
  a booking ID and reports the result back to the ashtangayoga.ie site.
- `index.php` is a full-screen web dashboard for the Pi showing the
  schedule, door state and a heating boost button.
- `bin` holds the start-up script, keep-alive and helper scripts.

## Tech

- Python 3 with FastAPI, python-kasa, PyP100, RPi.GPIO and Adafruit DHT
- PHP, jQuery and CSS for the dashboard
- Raspberry Pi

## Running

The files are meant to live in `/var/www/html` on the Pi.
`bin/doorpi.sh` starts Chromium in kiosk mode on the dashboard, then
starts `shala-manager.py`, the keep-alive script and the heating API.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
