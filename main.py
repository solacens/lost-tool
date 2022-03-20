import time
from glob import glob
from threading import Thread

import pydirectinput
from pynput.keyboard import Key, Listener
from win32gui import GetForegroundWindow, GetWindowText

KEY_FOR_HOLD = Key.ctrl_l

holding = False

def get_current_window_name():
  return GetWindowText(GetForegroundWindow())

def on_press(key):
  global holding
  if key == KEY_FOR_HOLD:
      holding = True

def on_release(key):
  global holding
  if key == KEY_FOR_HOLD:
    holding = False
  elif key == Key.insert:
    # Stop listener
    return False

class keyPress(Thread):
  global holding
  def __init__(self):
    Thread.__init__(self)
    self.daemon = True
    self.start()
  def run(self):
    while True:
      if "LOST ARK" in get_current_window_name() and holding:
        pydirectinput.press('g')
      time.sleep(0.1)

print("Hold {0} to G.".format(KEY_FOR_HOLD))
print("Press insert key to quit.")

# Start key press thread
keyPress()

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
