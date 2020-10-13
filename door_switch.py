#! /usr/bin/env python3
from gpiozero import Button
from time import sleep
from Adafruit_IO import Client, RequestError, Feed
from time import time
import logging as log
import os

# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = os.environ['ADAFRUIT_IO_KEY']

# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = os.environ['ADAFRUIT_IO_USERNAME']

def refresh_connection():
  # Create an instance of the REST client.
  global aio
  aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

  try:
      global door
      door = aio.feeds('door')
  except RequestError:
      log.critical('No feed called Door.')
      quit()

log.basicConfig(filename='/var/log/iot/door_switch.log',
                format='[%(levelname)s]%(asctime)s: %(message)s',
                level=log.INFO);
door_button = Button(4)
last_refresh = 0
log.info("Started door switch service.")
while True:
    if ((time() - last_refresh) > 1200):
      refresh_connection()
      last_refresh = time()
    log.info("Waiting for button to be pressed")
    door_button.wait_for_press(timeout=300)
    if (door_button.is_pressed):
      door_button.wait_for_release()
      log.info("Button was pressed.")
      log.info("Opening door...")
      aio.send_data(door.key, 'OPENED')
      sleep(1)
    else:
      log.info("Noone pressed the button for 5mins.");
