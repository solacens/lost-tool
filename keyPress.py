import time
from threading import Thread

import pydirectinput
from pynput.keyboard import Key
from win32gui import GetForegroundWindow, GetWindowText

class KeyPress(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.KEY_FOR_HOLD = Key.ctrl_l
    self.toggle_holding = True
    self.holding = False
    self.daemon = True
    self.start()
  def run(self):
    while True:
      if ("LOST ARK" in GetWindowText(GetForegroundWindow())) and self.toggle_holding and self.holding:
        pydirectinput.press('g')
      time.sleep(0.5)
