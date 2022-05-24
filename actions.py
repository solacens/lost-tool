from keyListener import KeyListener
from vision import Vision

import pyautogui
import time
import threading

DEBUG = True

class Actions:
  def __init__(self, gui):
    self.gui = gui
    self.log = gui.log
    # self.log = print

    self.vision = Vision()

    self.stopEvent = threading.Event()
    self.runningEvent = threading.Event()

    self.keyListener = KeyListener({
      '<ctrl>+<shift>+f': self.fishing,
      '<ctrl>+<shift>+s': self.stopAll
    })

    self.gui.connect("fishing", self.fishing)
    self.gui.connect("stop", self.stopAll)

    print("<Action> Initialized.")

  def stopAll(self):
    if (not self.stopEvent.is_set()) and self.runningEvent.is_set():
      self.log("STOPPING! Please wait for all actions done.", "Actions")
      self.stopEvent.set()

  def fishingOnce(self):
    self.log("Cast.", "Fishing")
    if not DEBUG:
      pyautogui.press("e")
    time.sleep(4)
    if not DEBUG:
      self.vision.waitTillFishingNotification()
    else:
      time.sleep(1)
    self.log("Pull.", "Fishing")
    if not DEBUG:
      pyautogui.press("e")

  def fishingThread(self):
    if self.runningEvent.is_set():
      return
    self.log("Starting in 2s.", "Fishing")
    self.runningEvent.set()
    self.vision.core.focus()
    time.sleep(2)

    while True:
      self.fishingOnce()
      if self.stopEvent.is_set():
        break
      else:
        self.log("Wait for next cast in 10s.", "Fishing")
        time.sleep(10)

    self.log("Stopped.", "Fishing")
    self.runningEvent.clear()
    self.stopEvent.clear()

  def fishing(self):
    th = threading.Thread(target=self.fishingThread)
    th.start()
    return th

if __name__ == "__main__":
  class GuiEmu:
    log = print

  action = Actions(GuiEmu())

  # Manually blocking
  action.keyListener.listener.join()
