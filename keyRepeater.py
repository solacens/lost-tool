from constants import *

from pynput.keyboard import Key, Listener
from win32gui import GetForegroundWindow, GetWindowText

import threading
import pyautogui
import time

class KeyRepeater:
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
        if LT_REPEATER_MINIMIUM_TIME is not None:
          timer = threading.Timer(LT_REPEATER_MINIMIUM_TIME, self.stopEvent.set)
          timer.start()
    def onRelease(key):
      if key == LT_REPEATER_KEY_FOR_HOLDING and (not self.stopEvent.is_set()):
        if LT_REPEATER_MINIMIUM_TIME is None:
          self.stopEvent.set()

    self.listener = Listener(on_press=onPress, on_release=onRelease)
    self.listener.start()

    print("<Key Repeater> Initialized.")

  def repeater(self):
    counter = 1
    while self.holdingEvent.is_set() and (not self.stopEvent.is_set()):
      pyautogui.press("g")
      counter = counter + 1
    self.holdingEvent.clear()
    self.stopEvent.clear()

if __name__ == "__main__":
  class GuiEmu:
    log = print
    connect = lambda _1, x, _2: print("Connect:", x)

  keyRepeater = KeyRepeater()

  # Any blocking function
  keyRepeater.listener.join()
