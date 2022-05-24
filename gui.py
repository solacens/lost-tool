from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime

from worker import Worker
from keyListener import KeyListener
from vision import VisionCore

import sys

STYLESHEET_TRANSPARENT = """
  QWidget{
    background-color: rgba(255,255,255,5%);
  }
  QTextEdit{
    background: rgba(255,255,255,10%);
    border: 1px solid rgba(125,125,125,30%);
  }
  QPushButton{
    background-color: rgba(255,255,255,35%)
  }
  QPushButton:hover{
    background-color: rgba(255,255,255,70%)
  }
"""
STYLESHEET_OPAQUE = """
  QWidget{
    background-color: rgba(255,255,255,80%);
  }
  QTextEdit{
    background: rgba(240,240,240,80%);
    border: 1px solid rgba(125,125,125,30%);
  }
  QPushButton{
    background-color: rgba(240,240,240,35%)
  }
  QPushButton:hover{
    background-color: rgba(0,0,0,20%)
  }
"""

GAME_WINDOW_RECT = VisionCore.getWindowRect()

PREFERRED_WIDTH = 300
PREFERRED_HEIGHT = 300

class GuiWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("LOST TOOL")
    self.setAttribute(Qt.WA_TranslucentBackground)
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    self.setGeometry((GAME_WINDOW_RECT[2] - PREFERRED_WIDTH), GAME_WINDOW_RECT[1], PREFERRED_WIDTH, PREFERRED_HEIGHT)

    font = QFont()
    font.setPointSize(8)
    font.setFamily("Consolas")

    buttonFont = QFont()
    buttonFont.setPointSize(8)
    buttonFont.setWeight(2)
    buttonFont.setFamily("Consolas")

    self.transparency_state = True
    self.listeners = {}

    self.bg = QWidget(self)
    self.bg.setStyleSheet(STYLESHEET_TRANSPARENT)
    self.bg.setMinimumSize(PREFERRED_WIDTH, PREFERRED_HEIGHT)

    layout = QGridLayout()
    layout.setContentsMargins(10, 10, 10, 10)

    ###########
    #
    #  Row 4
    #
    ###########
    self.textEdit = QTextEdit(self)
    self.textEdit.setReadOnly(True)
    self.textEdit.setFont(font)
    layout.addWidget(self.textEdit, 3, 0, 1, 3)

    ###########
    #
    #  Row 3
    #
    ###########
    clean_log_button = QPushButton()
    clean_log_button.setText("Clean logs")
    clean_log_button.setFont(buttonFont)
    clean_log_button.clicked.connect(lambda: self.textEdit.setPlainText(""))
    layout.addWidget(clean_log_button, 2, 2)

    ###########
    #
    #  Row 1
    #
    ###########
    key_repeater_button = QPushButton()
    key_repeater_button.setText("Key Repeater")
    key_repeater_button.setFont(buttonFont)
    self.listeners["key_repeater"] = key_repeater_button.clicked.connect
    layout.addWidget(key_repeater_button, 0, 0)

    fishing_button = QPushButton()
    fishing_button.setText("Fishing")
    fishing_button.setFont(buttonFont)
    self.listeners["fishing"] = fishing_button.clicked.connect
    layout.addWidget(fishing_button, 0, 1)

    excavating_button = QPushButton()
    excavating_button.setText("Excavating")
    excavating_button.setFont(buttonFont)
    excavating_button.setEnabled(False) # TODO
    self.listeners["excavating"] = excavating_button.clicked.connect
    layout.addWidget(excavating_button, 0, 2)

    ###########
    #
    #  Row 2
    #
    ###########
    chaos_button = QPushButton()
    chaos_button.setText("Chaos")
    chaos_button.setFont(buttonFont)
    chaos_button.setEnabled(False) # TODO
    self.listeners["chaos"] = chaos_button.clicked.connect
    layout.addWidget(chaos_button, 1, 0)

    ###########
    #
    #  Row 5
    #
    ###########
    stop_button = QPushButton()
    stop_button.setText("STOP!")
    stop_button.setFont(buttonFont)
    self.listeners["stop"] = stop_button.clicked.connect
    layout.addWidget(stop_button, 4, 0)

    transparency_button = QPushButton(self)
    transparency_button.setText("UI Transparency")
    transparency_button.setFont(buttonFont)
    transparency_button.clicked.connect(self.toggleTransparency)
    layout.addWidget(transparency_button, 4, 1)

    close_button = QPushButton(self)
    close_button.setText("Quit")
    close_button.setFont(buttonFont)
    self.listeners["quit"] = close_button.clicked.connect
    layout.addWidget(close_button, 4, 2)

    self.bg.setLayout(layout)
    self.show()

  def log(self, str, type = "Core"):
    now = datetime.now()
    self.textEdit.setPlainText("[{1} {3}] {0}\n{2}".format(str, type, self.textEdit.toPlainText(), now.strftime("%H:%M:%S")))

  def connect(self, name, func):
    if name in self.listeners:
      self.listeners[name](func)
      self.listeners.pop(name, None)
    else:
      print("Listener {0} not found.".format(name))

  def toggleHide(self):
    hidden = self.isHidden()
    if hidden:
      self.show()
    else:
      self.hide()

  def toggleTransparency(self):
    if self.transparency_state:
      self.bg.setStyleSheet(STYLESHEET_OPAQUE)
    else:
      self.bg.setStyleSheet(STYLESHEET_TRANSPARENT)
    self.transparency_state = not self.transparency_state

class Gui:
  def __init__(self):
    self.app = QApplication(sys.argv)
    self.window = GuiWindow()

    self.log = self.window.log
    self.connect = self.window.connect

    worker = Worker()
    worker.toggleHideSingal.connect(self.window.toggleHide)
    worker.start(self.keyListenerThread)
    self.connect("quit", self.app.exit)

    self.start = self.app.exec

    print("<GUI> Initialized.")

  def keyListenerThread(self, worker):
    keyListener = KeyListener({
      "<ctrl>+<shift>+q": self.app.exit,
      "<ctrl>+<shift>+h": worker.toggleHide
    })
    # The function itself run as a thread, so need to join the threads
    keyListener.listener.join()

if __name__ == "__main__":
  gui = Gui()

  gui.start()
