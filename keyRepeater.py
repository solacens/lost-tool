from constants import *

from pynput.keyboard import Key, Listener
from win32gui import GetForegroundWindow, GetWindowText

import threading
import pyautogui
import time

class KeyRepeater:
  toggleHolding = True

  holdingEvent = threading.Event()
  stopEvent = threading.Event()

  def __init__(self, gui):
    self.gui = gui

    def inWindow(text):
      return (text in GetWindowText(GetForegroundWindow()))

    def onPress(key):
      if key == LT_REPEATER_KEY_FOR_HOLDING and inWindow(LT_SEARCH_WINDOW_TITLE) and (not self.holdingEvent.is_set()) and (not self.stopEvent.is_set()):
        self.holdingEvent.set()
        th = threading.Thread(target=self.repeater, args=())
        th.start()

    def onRelease(key):
      if key == LT_REPEATER_KEY_FOR_HOLDING and (not self.stopEvent.is_set()):
        self.stopEvent.set()

    self.listener = Listener(on_press=onPress, on_release=onRelease)
    self.listener.start()

    self.gui.connect("key_repeater", self.toggleGPresser)

    print("<Key Repeater> Initialized.")

  def repeater(self):
    while self.holdingEvent.is_set() and (not self.stopEvent.is_set()):
      pyautogui.press("g")
      time.sleep(0.1)
    # Clear event after escape from loop
    self.holdingEvent.clear()
    self.stopEvent.clear()

  def toggleGPresser(self):
    self.toggleHolding = not self.toggleHolding
    self.log("Toggling.", "Key Repeater")
    self.log("Status now: {0}".format("On" if self.toggleHolding else "Off"), "Key Repeater")

if __name__ == "__main__":
  class GuiEmu:
    log = print
    connect = lambda _1, x, _2: print("Connect:", x)

  keyRepeater = KeyRepeater()

  # Any blocking function
