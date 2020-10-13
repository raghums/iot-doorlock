#! /usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep
from Adafruit_IO import Client, RequestError, Feed
import logging as log
import os

SOL_GATE = 12
# GPIO.setwarnings(False)

# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = os.environ['ADAFRUIT_IO_KEY']

# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = os.environ['ADAFRUIT_IO_USERNAME']

def refresh_connection():
  log.info("Refreshing connection.")
  # Create an instance of the REST client.
  global aio
  aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
  try:
    global door
    door = aio.feeds('door')
  except RequestError:
    log.critical('No feed called Door.')
    quit()

def open_door():
  log.info("Opening door.\n")
  try:
    log.info("Unlatching on for 5 secs.")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SOL_GATE, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(SOL_GATE, GPIO.HIGH)
    sleep(5)
    log.info("Releasing...")
    GPIO.setup(SOL_GATE, GPIO.IN)
    log.info("Sleeping for 1 sec.")
    sleep(1)
  except KeyboardInterrupt:
    log.critical("\n.Received keyboard interrupt.\n")
  finally:
    log.info("Cleaning up.")
    GPIO.setup(SOL_GATE, GPIO.IN)
    GPIO.cleanup()

log.basicConfig(filename='/var/log/iot/start_door_monitor.log',
                format='[%(levelname)s]%(asctime)s: %(message)s',
                level=log.INFO);
counter = 0
while(True):
  if (counter % 300 == 0):
    refresh_connection()
    counter = 0

  data = aio.receive(door.key)
  value = data.value
  log.info('Retrieved value of : {0}'.format(data.value))
  
  if (value == 'OPENED'):
    open_door()
    aio.send_data(door.key, 'CLOSED')
  else:
    sleep(1)
  counter += 1
