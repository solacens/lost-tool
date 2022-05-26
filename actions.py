from PyQt5.QtCore import *

from keyListener import KeyListener
from vision import Vision
from worker import Worker

import pyautogui
import time
import threading

# DEBUG = True
DEBUG = False

class Actions:
  def __init__(self, gui):
    self.gui = gui

    self.vision = Vision()

    self.stopEvent = threading.Event()
    self.runningEvent = threading.Event()

    self.keyListener = KeyListener({
      # "<ctrl>+<shift>+f": self.fishing,
      "<ctrl>+<shift>+s": self.stopAll
    })

    self.gui.connect("fishing", self.fishing)
    self.gui.connect("stop", self.stopAll)

    print("<Action> Initialized.")

  def stopAllThread(self, worker):
    if (not self.stopEvent.is_set()) and self.runningEvent.is_set():
      worker.log("Stopping! Please wait for all actions done.", "Actions")
      self.stopEvent.set()

  def stopAll(self):
    worker = Worker()
    worker.logSignal.connect(self.gui.log)
    worker.start(self.stopAllThread)

  def fishingThread(self, worker):
    if self.runningEvent.is_set():
      return
    worker.log("Starting in 2s.", "Fishing")
    self.runningEvent.set()
    time.sleep(2)

    while True:
      worker.log("Cast.", "Fishing")
      if not DEBUG:
        pyautogui.press("e")
      time.sleep(4)
      if not DEBUG:
        self.vision.waitTillFishingNotification()
      else:
        time.sleep(1)
      worker.log("Pull.", "Fishing")
      if not DEBUG:
        pyautogui.press("e")
      if self.stopEvent.is_set():
        break
      else:
        worker.log("Wait for next cast in 10s.", "Fishing")
        time.sleep(10)

    worker.log("Stopped.", "Fishing")
    self.runningEvent.clear()
    self.stopEvent.clear()

  def fishing(self):
    self.vision.core.focus()
    worker = Worker()
    worker.logSignal.connect(self.gui.log)
    worker.start(self.fishingThread)

if __name__ == "__main__":
  class GuiEmu:
    log = print
    connect = lambda _1, x, _2: print("Connect:", x)

  action = Actions(GuiEmu())

  # Manually blocking
  action.keyListener.listener.join()
