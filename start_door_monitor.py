#! /usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep
from Adafruit_IO import Client, RequestError, Feed

SOL_GATE = 12
# GPIO.setwarnings(False)

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '<key>'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = '<username>'

def refresh_connection():
  print("Refreshing connection.")
  # Create an instance of the REST client.
  global aio
  aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
  try:
    global door
    door = aio.feeds('door')
  except RequestError: # Doesn't exist, create a new feed
    # feed = Feed(name="foo")
    # foo = aio.create_feed(feed)
    print('No feed called Door.')
    quit()

def open_door():
  print("Opening door.\n")
  try:
    print("Unlatching on for 5 secs.")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SOL_GATE, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(SOL_GATE, GPIO.HIGH)
    sleep(5)
    print("Releasing...")
    GPIO.setup(SOL_GATE, GPIO.IN)
    print("Sleeping for 1 sec.")
    sleep(1)
  except KeyboardInterrupt:
    print("\n.Received keyboard interrupt.\n")
  finally:
    print("Cleaning up.")
    GPIO.setup(SOL_GATE, GPIO.IN)
    GPIO.cleanup()

counter = 0
while(True):
  if (counter % 300 == 0):
    refresh_connection()
    counter = 0

  data = aio.receive(door.key)
  value = data.value
  print('Retrieved value of : {0}'.format(data.value))
  
  if (value == 'OPENED'):
    open_door()
    aio.send_data(door.key, 'CLOSED')
  else:
    sleep(1)
  counter += 1
