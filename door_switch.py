#! /usr/bin/env python3
from gpiozero import Button
from time import sleep
from Adafruit_IO import Client, RequestError, Feed
from time import time

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '<key>'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = '<username>'

def refresh_connection():
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

door_button = Button(4)
last_refresh = 0
while True:
    print("Waiting for button to be pressed")
    door_button.wait_for_press()
    print("Button was pressed.")
    door_button.wait_for_release()
    if ((time() - last_refresh) > 300):
        refresh_connection()
        last_refresh = time()
    print("Opening door...")
    aio.send_data(door.key, 'OPENED')
    sleep(1)
